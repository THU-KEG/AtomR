import json
import time
import re
import os
import sys
from typing import Optional
from tqdm import tqdm
import traceback
from multiprocessing import Pool
import torch

from global_reasoner import GlobalReasoner
from prompts.tree_generation_prompts import format_tree_generation_prompt_hotpotqa, format_tree_generation_prompt_2wiki, format_tree_generation_prompt_musique, format_tree_generation_prompt_crag, format_tree_generation_prompt_blendqa
from prompts.answer_formulation_prompts import format_knowledge_source_selection_prompt
from query_knowledge_source.query_llm import OpenAICaller
from utils import extract_json_tree, extract_function_parameters, extract_ref_indices, find_qa_pairs_given_ref_indices, extract_knowledge_sources
from calculate_metrics import calculate_em, calculate_f1

NUM_PROCESSES = 4  # Concurrency for [build_trees_only] mode only

num_llm_calls = 0
num_text_retriever_calls = 0
num_web_retriever_calls = 0
num_kb_retriever_calls = 0
num_direct_Answer = 0
num_direct_RAG_func_failure = 0
num_direct_RAG_unknown = 0
num_Search_calls = 0
num_Relate_calls = 0
num_Filter_calls = 0
num_END_calls = 0
num_answer_from_child_qa_pairs_calls = 0

tree_generation_prompts = {
    'hotpotqa': format_tree_generation_prompt_hotpotqa,
    '2wiki': format_tree_generation_prompt_2wiki,
    'musique': format_tree_generation_prompt_musique,
    'crag': format_tree_generation_prompt_crag,
    'blendqa': format_tree_generation_prompt_blendqa
}


def print_results(em, cover_em, f1, num_total_entries, num_tree_parsing_failures, num_execution_failures, s):
    global num_llm_calls
    global num_text_retriever_calls
    global num_web_retriever_calls
    global num_kb_retriever_calls
    global num_direct_Answer
    global num_direct_RAG_func_failure
    global num_direct_RAG_unknown
    global num_Search_calls
    global num_Relate_calls
    global num_Filter_calls
    global num_END_calls
    global num_answer_from_child_qa_pairs_calls
    print("\n" + "*****" * 3 + " Evaluation Results " + "*****" * 3)
    print("Total num exact match:", em)
    print("Total num cover exact match:", cover_em)
    print("Total num entries:", num_total_entries)
    print("EM Score:", em / num_total_entries)
    print("Cover EM Score:", cover_em / num_total_entries)
    print("F1 Score:", f1 / num_total_entries)
    total_num_retriever_calls = num_text_retriever_calls + num_web_retriever_calls + num_kb_retriever_calls
    print("Total num_text_retriever_calls:", f"{num_text_retriever_calls}, {(num_text_retriever_calls/total_num_retriever_calls)*100:.2f}%")
    print("Total num_web_retriever_calls:", f"{num_web_retriever_calls}, {(num_web_retriever_calls/total_num_retriever_calls)*100:.2f}%")
    print("Total num_kb_retriever_calls:", f"{num_kb_retriever_calls}, {(num_kb_retriever_calls/total_num_retriever_calls)*100:.2f}%")
    print("Total num_llm_calls:", num_llm_calls)
    print("Total num_direct_Answer:", f"{num_direct_Answer}, {(num_direct_Answer/num_llm_calls)*100:.2f}%")
    print("Total num_direct_RAG_func_failure:", f"{num_direct_RAG_func_failure}, {(num_direct_RAG_func_failure/num_llm_calls)*100:.2f}%")
    print("Total num_direct_RAG_unknown:", f"{num_direct_RAG_unknown}, {(num_direct_RAG_unknown/num_llm_calls)*100:.2f}%")
    print("Total num_Search_calls:", f"{num_Search_calls}, {(num_Search_calls/num_llm_calls)*100:.2f}%")
    print("Total num_Relate_calls:", f"{num_Relate_calls}, {(num_Relate_calls/num_llm_calls)*100:.2f}%")
    print("Total num_Filter_calls:", f"{num_Filter_calls}, {(num_Filter_calls/num_llm_calls)*100:.2f}%")
    print("Total num_END_calls:", f"{num_END_calls}, {(num_END_calls/num_llm_calls)*100:.2f}%")
    print("Total num_answer_from_child_qa_pairs_calls:", f"{num_answer_from_child_qa_pairs_calls}, {(num_answer_from_child_qa_pairs_calls/num_llm_calls)*100:.2f}%")
    print("Total num_tree_parsing_failures:", num_tree_parsing_failures)
    print("Total num_execution_failures:", num_execution_failures)
    print("\nTotal time (seconds):", time.time() - s)


def build_reasoning_tree(dataset_name, q, q_index, reasoner: GlobalReasoner):
    prompt = tree_generation_prompts[dataset_name](q)
    llm_response, finish_reason = reasoner.openai_caller.query_gpt4o(prompt=prompt, max_tokens=512)
    if finish_reason == "length":  # if tree output too long, rerun with longer max_tokens
        llm_response, finish_reason = reasoner.openai_caller.query_gpt4o(prompt=prompt, max_tokens=768)
        print("build_reasoning_tree() finish_reason = \"length\", reran with max_tokens=768.")
    try:
        reasoning_tree = extract_json_tree(llm_response)
    except Exception as e:
        print(f"\n!!! Reasoning tree parsing error at question {q_index}: '{q}'")
        print(f"Error: {e}")
        print(f"LLM Response: {llm_response}")
        print("Saving reasoning_tree = \"TREE_PARSING_ERROR\".")
        return "TREE_PARSING_ERROR"
    
    return reasoning_tree


def build_tree_concurrently(dataset_name, entry, reasoner: GlobalReasoner):  # for multiprocessing
        question = entry["question"].strip()
        question_index = entry["index"]
        gold_answers = entry["answers"]
        reasoning_tree = build_reasoning_tree(dataset_name, question, question_index, reasoner)
        
        return {"index": question_index, "question": question, "gold": gold_answers, "reasoning_tree": reasoning_tree}
    

def postorder_traversal(question_tree, node):  # performs post-order traversal recursively
    results = []
    children = question_tree.get(node, [])
    current_node_dict = {}
    
    if isinstance(children, list):
        child_questions = []
        for child in children:
            child_result = postorder_traversal(question_tree, child)
            results.extend(child_result)
            child_questions.append(child)
        current_node_dict[node] = child_questions  # append child questions for non-leaf nodes
    else:
        current_node_dict[node] = children  # append leaf function/[END] mark for leaf nodes
        
    results.append(current_node_dict) 
    
    return results


def convert_question_tree_to_list(question_tree, q, q_index):  
    try:
        root_question = next(iter(question_tree))
        ordered_questions = postorder_traversal(question_tree, root_question)
    except Exception as e:
        raise Exception(f"!!! Postorder question list convertion error at question {q_index}: '{q}'\nError: {e}")
    
    return ordered_questions


def execute_postorder_q_list(reasoner: GlobalReasoner, dataset_name: str, reasoning_tree: dict, postorder_q_list: list, q_index: Optional[int] = 0, gold: Optional[list] = None):
    global num_llm_calls
    global num_text_retriever_calls
    global num_web_retriever_calls
    global num_kb_retriever_calls
    global num_direct_Answer
    global num_direct_RAG_func_failure
    global num_direct_RAG_unknown
    global num_Search_calls
    global num_Filter_calls
    global num_Relate_calls
    global num_END_calls
    global num_answer_from_child_qa_pairs_calls
    
    num_llm_calls_before_cur_entry = num_llm_calls
    
    """ 
    Local helper functions 
    """
    
    def extract_index_from_dict(d):
        key = next(iter(d.keys()))
        match = re.search(r'^(\d+)\.', key)
        return int(match.group(1)) if match else float('inf')
            
            
    def execute_select_knowledge_sources(reasoner, question, q_ref_indices, ref_qa_list):
        print("entered select_knowledge_sources()")
        print("ref_qa_list:", ref_qa_list)
        global num_llm_calls
        if len(reasoner.available_knowledge_sources) <= 2:  # directly use available knowledge sources if less than 2 available
            selected_knowledge_sources = reasoner.available_knowledge_sources
        else:  # let LLM planner select knowledge sources
            temp_q_for_knowledge_selection = question  # format temporary question for knowledge source selection  
            try:
                for ref in q_ref_indices:
                    temp_q_for_knowledge_selection = temp_q_for_knowledge_selection.replace(ref, ref_qa_list[ref]["answers"][0])  # simply replace each ref index with first answer
                print("temp_q_for_knowledge_selection:", temp_q_for_knowledge_selection)
                prompt = format_knowledge_source_selection_prompt(temp_q_for_knowledge_selection, reasoner.available_knowledge_sources)
                llm_response, finish_reason = reasoner.openai_caller.query_gpt4o(prompt=prompt, max_tokens=64)
                num_llm_calls += 1
                selected_knowledge_sources = extract_knowledge_sources(llm_response, reasoner.available_knowledge_sources)
            except Exception as e:
                print("!!! [Knowledge source selection failure]:", e)
                print("Setting selected_knowledge_sources=reasoner.available_knowledge_sources.")
                selected_knowledge_sources = reasoner.available_knowledge_sources
                    
        print("Selected knowledge sources:", selected_knowledge_sources)
        return selected_knowledge_sources
    
    
    def execute_direct_RAG(question, q_ref_indices, ref_qa_list, selected_knowledge_sources, direct_rag_for_unknown=False):
        global num_direct_RAG_func_failure, num_direct_RAG_unknown, num_llm_calls, num_text_retriever_calls, num_web_retriever_calls, num_kb_retriever_calls
        if (direct_rag_for_unknown):
            print("(entered direct_RAG() due to empty child aggregation answer)")
        else:
            print("(entered direct_RAG() due to function execution failure)")
        print("question:", question)
                    
        if selected_knowledge_sources is None:
            print("selected_knowledge_sources is None, calling execute_select_knowledge_sources()")
            selected_knowledge_sources = execute_select_knowledge_sources(reasoner, question, q_ref_indices, ref_qa_list)
                    
        # Rewrite questions with ref indices
        directRAG_questions_rewritten = []
        if "among" in question.lower():  # likely filter question, directly replace ref index with answer list
            question_rewritten_ans_lists = question
            for ref in q_ref_indices:
                question_rewritten_ans_lists = question_rewritten_ans_lists.replace(ref, str(ref_qa_list[ref]["answers"]))
            directRAG_questions_rewritten.append(question_rewritten_ans_lists)
        else:  # non-filter questions
            if len(q_ref_indices) == 0:
                directRAG_questions_rewritten.append(question)
            elif len(q_ref_indices) == 1:
                ref = q_ref_indices[0]
                ref_answers = ref_qa_list[ref]["answers"]
                for ans in ref_answers:
                    directRAG_questions_rewritten.append(question.replace(ref, ans))  # rewrite question with each possible ref answer
            elif len(q_ref_indices) == 2:  # supports maximum 2 ref indices
                ref1 = q_ref_indices[0]
                ref2 = q_ref_indices[1]
                ref_answers_1 = ref_qa_list[ref1]["answers"]
                ref_answers_2 = ref_qa_list[ref2]["answers"]
                for ans1 in ref_answers_1:  # rewrite question with each possible double ref answer combinations
                    for ans2 in ref_answers_2:
                        cur_question_rewritten = question.replace(ref1, ans1)
                        cur_question_rewritten = cur_question_rewritten.replace(ref2, ans2)
                        directRAG_questions_rewritten.append(cur_question_rewritten)  
            else:  # >= 3 indices, directly formulate single question_rewritten by replacing each question index with answer list
                question_rewritten_ans_lists = question
                for ref in q_ref_indices:
                    question_rewritten_ans_lists = question_rewritten_ans_lists.replace(ref, str(ref_qa_list[ref]["answers"]))
                directRAG_questions_rewritten.append(question_rewritten_ans_lists)
                    
        for question_rewritten in directRAG_questions_rewritten:
            print("direct_RAG() cur_question_rewritten:", question_rewritten)
                        
            clean_answer_list, paraphrase_answer, supporting_knowledge = reasoner.direct_RAG(dataset_name, selected_knowledge_sources, question_rewritten)
            print("clean_answer_list:", clean_answer_list)
            print("paraphrase_answer:", paraphrase_answer)
                        
            # Store answers to global answer dict
            global_qa_dict_combined_answers[question]["clean_answer_list"] += clean_answer_list
            global_qa_dict_combined_answers[question]["paraphrase_answer"] += f"{paraphrase_answer}; "
            global_qa_dict[question]["clean_answer_list"].append(clean_answer_list)
            global_qa_dict[question]["paraphrase_answer"].append(paraphrase_answer)
            global_qa_dict[question]["supporting_knowledge"].append(supporting_knowledge)
                        
            # Update statistics
            if direct_rag_for_unknown:
                num_direct_RAG_unknown += 1
            else:
                num_direct_RAG_func_failure += 1
            num_llm_calls += 1
            if "Text" in selected_knowledge_sources:
                num_text_retriever_calls += 1
            if "Web" in selected_knowledge_sources:
                num_web_retriever_calls += 1
            if "KB" in selected_knowledge_sources:
                num_kb_retriever_calls += 1
    
    """
    Main logic
    """
    
    root_question = next(iter(postorder_q_list[-1].keys()))  
    
    print("\n" + "======" * 6)
    print(f"Question {q_index}:", root_question)
    if gold is not None:
        print("Gold:", gold)
        
    print("\n*** Step 1 'build_reasoning_tree' (completed) ***")
    print("Reasoning Tree:", reasoning_tree)
    
    print("\n*** Step 2 'convert_question_tree_to_list' (completed) ***")
    print("Postorder Question List:", postorder_q_list)
    
    print("\n*** Step 3 'execute_postorder_q_list' ***")
    
    global_qa_dict = {}  # stores sub-questions and answers for the whole reasoning tree
    global_qa_dict_combined_answers = {}  # combines all sub-answers for each sub-question
    
    for node in postorder_q_list:
        (question, children), = node.items()
        print("\nQuestion:", question)
        print("Children:", children)
        
        # Initialize answer dicts and selected knowledge sources
        global_qa_dict[question] = {}
        global_qa_dict[question]["clean_answer_list"] = []
        global_qa_dict[question]["paraphrase_answer"] = []
        global_qa_dict[question]["supporting_knowledge"] = []
        global_qa_dict[question]["function"] = "N/A"
        global_qa_dict_combined_answers[question] = {} 
        global_qa_dict_combined_answers[question]["paraphrase_answer"] = ""
        global_qa_dict_combined_answers[question]["clean_answer_list"] = []
        selected_knowledge_sources = None  
        
        # Extract [Question ref indices] and record ref indices with actual answers
        q_ref_indices = extract_ref_indices(question) 
        ref_qa_list, ref_qa_paraphrase = find_qa_pairs_given_ref_indices(q_ref_indices, global_qa_dict_combined_answers)
        
        ##### Execute Node 
        
        ### Case A - current node is a leaf node with an atomic function
        if isinstance(children, str) and '[END]' not in children:  
            function_str = children
            
            ### Select external knowledge sources
            selected_knowledge_sources = execute_select_knowledge_sources(reasoner, question, q_ref_indices, ref_qa_list)
            
            ### Parse and execute function, redirects to direct_RAG() if function execution fails
            try:  
                function_parameters = extract_function_parameters(function_str)  
                global_qa_dict[question]["function"] = function_str
                
                ### Extract [Fun tion ref indices] and update ref_qa_list
                func_ref_indices = extract_ref_indices(function_str)  # question and function may refer to different indices, need to extract indices from both
                all_ref_indices_set = set(q_ref_indices + func_ref_indices)
                ref_qa_list, ref_qa_paraphrase = find_qa_pairs_given_ref_indices(all_ref_indices_set, global_qa_dict_combined_answers)
            
                ### Call Search() function
                if function_str.lower().startswith("search"):
                    
                    def execute_Search(question, function_str, function_parameters):
                        global num_llm_calls, num_Search_calls, num_text_retriever_calls, num_web_retriever_calls, num_kb_retriever_calls
                        print("\n(entered Search() function)")
                        print("function_str:", function_str)
                        print("function_parameters:", function_parameters)

                        # Check function parameters
                        if not (len(function_parameters) == 1 or len(function_parameters) == 2):
                            raise Exception(f"Invalid number of function parameters: expected 1 or 2, got {len(function_parameters)}.\nfunction_str: {function_str}")
                        
                        # Initialize question and parameters that may need ref index replacement
                        question_template = question
                        head_entity_param_template = function_parameters[0]
                        descriptor_param_template = ""
                        
                        # Get head entities
                        head_entity_refs = []  # referenced answers in head entity param
                        head_entity_ref_idx_list = extract_ref_indices(function_parameters[0])
                        print("head_entity_ref_idx_list:", head_entity_ref_idx_list)
                        if len(head_entity_ref_idx_list) == 0:  # first func parameter is entity name string
                            head_entity_refs = [function_parameters[0]]
                        elif len(head_entity_ref_idx_list) == 1:   # first func parameter contains ref index, needs entity replacement
                            ref = head_entity_ref_idx_list[0]
                            head_entity_refs = ref_qa_list[ref]["answers"]
                            question_template = question_template.replace(ref, "[HEAD]")
                            head_entity_param_template = head_entity_param_template.replace(ref, "[HEAD]")
                        else:
                            raise Exception(f"Invalid number of ref indices for Search() parameter 1 \"entity_name\": expected 0 or 1, got {len(head_entity_ref_idx_list)}.\nfunction_str: {function_str}")
                        
                        # Get descriptors      
                        str_descriptor_refs = []  # referenced answers in descriptor param
                        if len(function_parameters) == 1:  # no descriptors
                            str_descriptor_refs = [""]
                        elif len(function_parameters) == 2:  # contains descriptors
                            descriptor_ref_idx_list = extract_ref_indices(function_parameters[1])
                            print("descriptor_ref_idx_list:", descriptor_ref_idx_list)
                            if len(descriptor_ref_idx_list) == 0:  # descriptor doesn't contain ref index
                                str_descriptor_refs = [function_parameters[1]]
                                descriptor_param_template = function_parameters[1]
                            elif len(descriptor_ref_idx_list) == 1:  # descriptor contains ref index
                                ref = descriptor_ref_idx_list[0]
                                str_descriptor_refs = ref_qa_list[ref]["answers"]
                                question_template = question_template.replace(ref, "[DES]")
                                descriptor_param_template = function_parameters[1].replace(ref, "[DES]")
                            else:
                                raise Exception(f"Invalid number of ref indices for Search() parameter 2 \"descriptor\": expected 0 or 1, got {len(descriptor_ref_idx_list)}.\nfunction_str: {function_str}")
                        
                        print("question_template:", question_template)
                        print("head_entity_param_template:", head_entity_param_template)
                        print("descriptor_param_template:", descriptor_param_template)
                        print("\nhead_entity_refs:", head_entity_refs)
                        print("str_descriptor_refs:", str_descriptor_refs)
                        
                        # Execute function
                        for entity in head_entity_refs:
                            for descriptor in str_descriptor_refs:
                                # Prepare function parameters
                                cur_question = question_template.replace("[HEAD]", entity)
                                cur_question = cur_question.replace("[DES]", descriptor)
                                cur_head_entity_param = head_entity_param_template.replace("[HEAD]", entity)
                                cur_descriptor_param = descriptor_param_template.replace("[DES]", descriptor)
                                # Append descriptor to question if not already included
                                if cur_descriptor_param != "" and cur_descriptor_param.lower() not in cur_question.lower():  
                                    cur_question = f"{cur_question} ({cur_descriptor_param})"
                                print("\nSearch() cur_question:", cur_question)
                                print("Function params:", f"(\"{cur_head_entity_param}\", \"{cur_descriptor_param}\")")
                                
                                # Call function
                                clean_answer_list, paraphrase_answer, supporting_knowledge = reasoner.Search(dataset_name, selected_knowledge_sources, cur_question, cur_head_entity_param, cur_descriptor_param)
                                print("clean_answer_list:", clean_answer_list)  
                                print("paraphrase_answer:", paraphrase_answer)  
                                
                                # Store answers to global answer dict
                                global_qa_dict_combined_answers[question]["clean_answer_list"] += clean_answer_list
                                global_qa_dict_combined_answers[question]["paraphrase_answer"] += f"{paraphrase_answer}; "
                                global_qa_dict[question]["clean_answer_list"].append(clean_answer_list)
                                global_qa_dict[question]["paraphrase_answer"].append(paraphrase_answer)
                                global_qa_dict[question]["supporting_knowledge"].append(supporting_knowledge)
                                
                                # Update statistics
                                num_Search_calls += 1
                                num_llm_calls += 1
                                if "Text" in selected_knowledge_sources:
                                    num_text_retriever_calls += 1
                                if "Web" in selected_knowledge_sources:
                                    num_web_retriever_calls += 1
                                if "KB" in selected_knowledge_sources:
                                    num_kb_retriever_calls += 1
                                    
                                    
                    execute_Search(question, function_str, function_parameters)
                    
                ### Call Relate() function  
                elif function_str.lower().startswith("relate"):
                    
                    def execute_Relate(question, function_str, function_parameters):
                        global num_llm_calls, num_Relate_calls, num_text_retriever_calls, num_web_retriever_calls, num_kb_retriever_calls
                        print("\n(entered Relate() function)")
                        print("function_str:", function_str)
                        print("function_parameters:", function_parameters)
                        
                        # Check function parameters
                        if not len(function_parameters) == 2:
                            raise Exception(f"Invalid number of function parameters: expected 2, got {len(function_parameters)}.\nfunction_str: {function_str}")
                        
                        # Initialize question and parameters that may need ref index replacement
                        question_template = question
                        head_entity_param_template = function_parameters[0]
                        relation_param_template = function_parameters[1]
                        
                        # Get head entities
                        head_entity_refs = []  # referenced answers in head entity param
                        head_entity_ref_idx_list = extract_ref_indices(function_parameters[0])
                        print("head_entity_ref_idx_list:", head_entity_ref_idx_list)
                        if len(head_entity_ref_idx_list) == 0:  # first func parameter is entity name string
                            head_entity_refs = [function_parameters[0]]
                        elif len(head_entity_ref_idx_list) == 1:   # first func parameter contains ref index, needs entity replacement
                            ref = head_entity_ref_idx_list[0]
                            head_entity_refs = ref_qa_list[ref]["answers"]
                            question_template = question_template.replace(ref, "[HEAD]")
                            head_entity_param_template = head_entity_param_template.replace(ref, "[HEAD]")
                        else:
                            raise Exception(f"Invalid number of ref indices for Relate() parameter 1 \"entity_name\": expected 0 or 1, got {len(head_entity_ref_idx_list)}.\nfunction_str: {function_str}")
                        
                        # Get relations      
                        relation_refs = []  # referenced answers in relation param
                        relations_ref_idx_list = extract_ref_indices(function_parameters[1])
                        print("relations_ref_idx_list:", relations_ref_idx_list)
                        if len(relations_ref_idx_list) == 0:  # relation doesn't contain ref index
                            relation_refs = [function_parameters[1]]
                            relation_param_template = function_parameters[1]
                        elif len(relations_ref_idx_list) == 1:  # relation contains one ref index
                            ref = relations_ref_idx_list[0]
                            relation_refs = ref_qa_list[ref]["answers"]
                            question_template = question_template.replace(ref, "[REL]")
                            relation_param_template = relation_param_template.replace(ref, "[REL]")
                        else:
                            raise Exception(f"Invalid number of ref indices for Relate() parameter 2 \"relation\": expected 0 or 1, got {len(relations_ref_idx_list)}.\nfunction_str: {function_str}")
                        
                        # Reformat question (might contain different refs compared to function, reformatting just in case)
                        q_template_ref_indices = extract_ref_indices(question_template)  # extract any additional ref indices
                        for ref in q_template_ref_indices: 
                            question_template = question_template.replace(ref, ref_qa_list[ref]["answers"][0])  # TODO: only extracting first answer for now, should be enough
                        
                        print("question_template:", question_template)
                        print("head_entity_param_template:", head_entity_param_template)
                        print("relation_param_template:", relation_param_template)
                        print("\nhead_entity_refs:", head_entity_refs)
                        print("relation_refs:", relation_refs)
                        
                        # Execute function
                        for entity in head_entity_refs:
                            for relation in relation_refs:
                                # Prepare function parameters
                                cur_question = question_template.replace("[HEAD]", entity)
                                cur_question = cur_question.replace("[REL]", relation)
                                cur_head_entity_param = head_entity_param_template.replace("[HEAD]", entity)
                                cur_relation_param = relation_param_template.replace("[REL]", relation)
                                print("\nRelate() cur_question:", cur_question)
                                print("Function params:", f"(\"{cur_head_entity_param}\", \"{cur_relation_param}\")")
                                
                                # Call function
                                clean_answer_list, paraphrase_answer, supporting_knowledge = reasoner.Relate(dataset_name, selected_knowledge_sources, cur_question, cur_head_entity_param, cur_relation_param)                           
                                print("clean_answer_list:", clean_answer_list) 
                                print("paraphrase_answer:", paraphrase_answer) 
                                
                                # Store answers to global answer dict
                                global_qa_dict_combined_answers[question]["clean_answer_list"] += clean_answer_list
                                global_qa_dict_combined_answers[question]["paraphrase_answer"] += f"{paraphrase_answer}; "
                                global_qa_dict[question]["clean_answer_list"].append(clean_answer_list)
                                global_qa_dict[question]["paraphrase_answer"].append(paraphrase_answer)
                                global_qa_dict[question]["supporting_knowledge"].append(supporting_knowledge)
                                
                                # Update statistics
                                num_Relate_calls += 1 
                                num_llm_calls += 1
                                if "Text" in selected_knowledge_sources:
                                    num_text_retriever_calls += 1
                                if "Web" in selected_knowledge_sources:
                                    num_web_retriever_calls += 1
                                if "KB" in selected_knowledge_sources:
                                    num_kb_retriever_calls += 1
                    
                    execute_Relate(question, function_str, function_parameters)
                        
                ### Call Filter() function    
                elif function_str.lower().startswith("filter"):
                    def execute_Filter(question, function_str, function_parameters):
                        global num_Filter_calls, num_llm_calls, num_text_retriever_calls, num_web_retriever_calls, num_kb_retriever_calls
                        print("\n(entered Filter() function)")
                        print("function_str:", function_str)
                        print("function_parameters:", function_parameters)
                        
                        # Check parameters
                        if not len(function_parameters) == 2:
                            raise Exception(f"Invalid number of function parameters: expected 2, got {len(function_parameters)}.\nfunction_str: {function_str}")
                        
                        # Initialize question and parameters that may need ref index replacement
                        question_template = question
                        head_entities_param_template = function_parameters[0]
                        condition_param_template = function_parameters[1]
                            
                        # Get head entities
                        head_entities_refs = []  # referenced answers in head entities param
                        head_entities_ref_idx_list = extract_ref_indices(function_parameters[0])
                        print("head_entities_ref_idx_list:", head_entities_ref_idx_list)
                        if len(head_entities_ref_idx_list) == 0:  # first func parameter doesn't contain ref index
                            head_entities_refs = [function_parameters[0]]
                        elif len(head_entities_ref_idx_list) == 1:   # first func parameter contains ref index, needs entity replacement
                            ref = head_entities_ref_idx_list[0]
                            head_entities_refs = ref_qa_list[ref]["answers"]
                            # for Filter() function, directly replace entity ref with serialized list of entities
                            question_template = question_template.replace(ref, ", ".join(head_entities_refs))
                            head_entities_param_template = head_entities_param_template.replace(ref, ", ".join(head_entities_refs))
                        else:
                            raise Exception(f"Invalid number of ref indices for Filter() parameter 1 \"entities\": expected 0 or 1, got {len(head_entities_ref_idx_list)}.\nfunction_str: {function_str}")
                        
                        # Get conditions   
                        condition_refs = []  # referenced answers in relation param
                        conditions_ref_idx_list = extract_ref_indices(function_parameters[1])
                        print("conditions_ref_idx_list:", conditions_ref_idx_list)
                        if len(conditions_ref_idx_list) == 0:  # relation doesn't contain ref index
                            condition_refs = [function_parameters[1]]
                        elif len(conditions_ref_idx_list) == 1:  # relation contains one ref index
                            ref = conditions_ref_idx_list[0]
                            condition_refs = ref_qa_list[ref]["answers"]
                            question_template = question_template.replace(ref, "[COND]")
                            condition_param_template = condition_param_template.replace(ref, "[COND]")
                        else:
                            raise Exception(f"Invalid number of ref indices for Filter() parameter 2 \"condition\": expected 0 or 1, got {len(conditions_ref_idx_list)}.\nfunction_str: {function_str}")
                        
                        print("question_template:", question_template)
                        print("head_entities_param_template:", head_entities_param_template)
                        print("condition_param_template:", condition_param_template)
                        print("\nhead_entities_refs:", head_entities_refs)
                        print("condition_refs:", condition_refs)
                            
                        # Execute function
                        cur_head_entities_param = head_entities_param_template  # static head entities for Filter(); only used for printing debug messages
                        for condition in condition_refs:
                            # Prepare function parameters
                            cur_question = question_template.replace("[COND]", condition)
                            cur_condition_param = condition_param_template.replace("[COND]", condition)
                            # Append condition to question if not already included
                            if cur_condition_param != "" and cur_condition_param.lower() not in cur_question.lower():  
                                cur_question = f"{cur_question} (Filter condition: {cur_condition_param})"
                            print("\nFilter() cur_question:", cur_question)
                            print("Function params:", f"(\"{cur_head_entities_param}\", \"{cur_condition_param}\")")
                            
                            clean_answer_list, paraphrase_answer, supporting_knowledge = reasoner.Filter(dataset_name, selected_knowledge_sources, cur_question, head_entities_refs, cur_condition_param)
                            print("clean_answer_list:", clean_answer_list)  
                            print("paraphrase_answer:", paraphrase_answer)   
                                    
                            # Store answers to global answer dict
                            global_qa_dict_combined_answers[question]["clean_answer_list"] += clean_answer_list
                            global_qa_dict_combined_answers[question]["paraphrase_answer"] += f"{paraphrase_answer}; "
                            global_qa_dict[question]["clean_answer_list"].append(clean_answer_list)
                            global_qa_dict[question]["paraphrase_answer"].append(paraphrase_answer)
                            global_qa_dict[question]["supporting_knowledge"].append(supporting_knowledge)
                            
                            # Update statistics
                            num_Filter_calls += 1 
                            num_llm_calls += 1
                            if "Text" in selected_knowledge_sources:
                                num_text_retriever_calls += 1
                            if "Web" in selected_knowledge_sources:
                                num_web_retriever_calls += 1
                            if "KB" in selected_knowledge_sources:
                                num_kb_retriever_calls += 1
                        
                    execute_Filter(question, function_str, function_parameters)
                    
            except Exception as e:  # if function execution failed, use direct_RAG() to answer
                print("\n!!! [Function Execution failure]:", function_str)
                print("Exception:", e)
                print("Traceback:", traceback.format_exc())                
                
                execute_direct_RAG(question, q_ref_indices, ref_qa_list, selected_knowledge_sources, direct_rag_for_unknown=False)
                    
        ### Non-leaf node or [END] leaf node, answer using child/sibling QA pairs
        elif (isinstance(children, list) and len(children) > 0) or (isinstance(children, str) and '[END]' in children):  
            child_qa_pairs_list = []
            is_childQA = False  # flag to denote child aggregation QA (apart from [END] ref aggregation answer)
            
            # Case (1): Non-leaf node, answer from child QA pairs
            if isinstance(children, list):  
                for child in children:
                    child_q = child
                    try:
                        child_clean_answer_list = global_qa_dict_combined_answers[child_q]["clean_answer_list"]
                        child_paraphrase_answer = global_qa_dict_combined_answers[child_q]["paraphrase_answer"]
                    except Exception as e:
                        raise Exception(f"!!! Child question '{child_q}' not found in global_qa_dict.\nError: {e}")
                    child_qa_pairs_list.append({"question": child_q, "clean_answer_list": child_clean_answer_list, "paraphrase_answer": child_paraphrase_answer})
                is_childQA = True
                num_answer_from_child_qa_pairs_calls += 1
            
            # Case (2): [END] leaf node, answer from ref QA pairs
            else:  
                for ref in q_ref_indices:
                    ref_q = ref_qa_list[ref]["question"]
                    ref_clean_answer_list = ref_qa_list[ref]["answers"]
                    ref_paraphrase_answer = ref_qa_paraphrase[ref]["answers"] 
                    child_qa_pairs_list.append({"question": ref_q, "clean_answer_list": ref_clean_answer_list, "paraphrase_answer": ref_paraphrase_answer})
                num_END_calls += 1
                        
            # Format and augment child qa pairs
            child_qa_pairs_formatted = []
            added_child_q = set()  # record added child questions to avoid duplication during cross layer recordings
            for qa_pair in child_qa_pairs_list:
                child_q = qa_pair["question"]
                child_clean_answer_list = qa_pair["clean_answer_list"]
                child_paraphrase_answer = qa_pair["paraphrase_answer"]
                child_q_ref_indices = extract_ref_indices(child_q)
                if len(child_q_ref_indices) == 0:
                    child_qa_pairs_formatted.append({child_q: str(child_clean_answer_list)})  # no ref idx = no ambiguity, only append clean answer list
                    added_child_q.add(child_q)
                else:
                    child_qa_pairs_formatted.append({child_q: child_paraphrase_answer + ". " + str(child_clean_answer_list)})  # append paraphrase answer + clean answer list
                    added_child_q.add(child_q)
                    # Also append qa pairs referenced in child questions
                    child_cross_layer_ref_qa_list, child_cross_layer_ref_qa_paraphrase = find_qa_pairs_given_ref_indices(child_q_ref_indices, global_qa_dict_combined_answers)
                    for cross_layer_ref in child_q_ref_indices:
                        cross_layer_ref_q = child_cross_layer_ref_qa_list[cross_layer_ref]["question"]
                        if cross_layer_ref_q not in added_child_q:  # avoid duplication
                            child_qa_pairs_formatted.append({cross_layer_ref_q: str(child_cross_layer_ref_qa_list[cross_layer_ref]["answers"])})  # clean answer list should be enough
            
            child_qa_pairs_formatted = sorted(child_qa_pairs_formatted, key=extract_index_from_dict)  # sort in ascending index order
            print("child_qa_pairs_formatted:", child_qa_pairs_formatted)
            
            # Call function
            clean_answer_list, paraphrase_answer, supporting_knowledge = reasoner.AnswerFromQAPairs(dataset_name, question, child_qa_pairs_formatted)
            print("clean_answer_list:", clean_answer_list)
            print("paraphrase_answer:", paraphrase_answer)
            
            num_llm_calls += 1
            
            # call direct_RAG() if childQA yields empty answer
            if is_childQA and (paraphrase_answer.lower().strip() == "unknown" or len(clean_answer_list) == 0):
                print("\n!!! [Empty answer for ChildQA]")
                    
                execute_direct_RAG(question, q_ref_indices, ref_qa_list, selected_knowledge_sources, direct_rag_for_unknown=True)
                continue  # cur node's answers already stored in execute_direct_RAG() function, can continue to next node
                                
            # Store answers to global answer dict
            global_qa_dict_combined_answers[question]["clean_answer_list"] += clean_answer_list
            global_qa_dict_combined_answers[question]["paraphrase_answer"] += f"{paraphrase_answer}; "

            global_qa_dict[question]["clean_answer_list"].append(clean_answer_list)
            global_qa_dict[question]["paraphrase_answer"].append(paraphrase_answer)
            global_qa_dict[question]["supporting_knowledge"].append(supporting_knowledge)
                        
        else:  # use direct_RAG() for empty child or unknown child type
            execute_direct_RAG(question, q_ref_indices, ref_qa_list, selected_knowledge_sources, direct_rag_for_unknown=True)
            
        
        cur_ans_paraphrase = global_qa_dict_combined_answers[question]["paraphrase_answer"]
        if len(cur_ans_paraphrase) >= 2 and cur_ans_paraphrase[-2:] == "; ": 
            cur_ans_paraphrase = cur_ans_paraphrase[:-2]  # remove last "; " for paraphrase_answer
            global_qa_dict_combined_answers[question]["paraphrase_answer"] = cur_ans_paraphrase
    
    
    ### Formulate final answer
    final_answer_list = global_qa_dict_combined_answers[root_question]["clean_answer_list"]
    final_answer_paraphrase = global_qa_dict_combined_answers[root_question]["paraphrase_answer"]
    
    if len(final_answer_list) == 0:  # if final answer is empty, call LLM to directly answer
        print("!!! final_answer_list = [], calling direct_Answer().")
        print("question:", root_question)
        final_answer_list, final_answer_paraphrase = reasoner.direct_Answer(dataset_name, root_question)
        print("final_answer_list:", final_answer_list)
        print("final_answer_paraphrase:", final_answer_paraphrase)
        
        global_qa_dict_combined_answers[root_question]["supporting_knowledge"] = "direct_Answer()"
        global_qa_dict[root_question]["supporting_knowledge"].append("direct_Answer()")
        num_llm_calls += 1
        num_direct_Answer += 1
    
    print("\n===================== Final Answer =====================") 
    print("Question:", root_question) 
    print("Full Postorder Reasoning Path: ")
    for sub_q in global_qa_dict:
        clean_answer_list = global_qa_dict_combined_answers[sub_q]["clean_answer_list"]
        function = global_qa_dict[sub_q]["function"]
        supporting_knowledge = global_qa_dict[sub_q]["supporting_knowledge"]
        print("Question:", sub_q)
        print("Clean Answer List:", clean_answer_list)
        print("Function Call:", function)
        print("Supporting Knowledge:", supporting_knowledge)
        print()
    
    print("Paraphrase Answer:", final_answer_paraphrase)
    
    # format Predicted Answer list into single string
    predicted_answer = ", ".join(str(entry) for entry in final_answer_list)
    print("Predicted Answer:", predicted_answer)
    if gold is not None:
        print("Gold:", gold)
    
    print("num_llm_calls for cur question execution:", num_llm_calls - num_llm_calls_before_cur_entry)
    return predicted_answer, global_qa_dict_combined_answers, global_qa_dict
    

### Function to run single query
def run_query(reasoner: GlobalReasoner, dataset_name: str, question: str, q_index: Optional[int] = 0, gold: Optional[list] = None, 
              build_tree_only: Optional[bool] = False, execute_tree_only: Optional[bool] = False, 
              input_tree: Optional[str] = None):
        
    if (int(build_tree_only) + int(execute_tree_only)) != 1:
        raise Exception("Need to set exactly one mode to True: ['build_tree_only', 'execute_tree_only']")
    
    if (execute_tree_only and input_tree is None):
        raise Exception("\"execute_tree_only\" mode selected, but \"input_tree\" is None.")
    
    question = question.strip()  # remove possible extra spaces
    
    # Set default return values
    reasoning_tree = None
    postorder_q_list = None
    predicted_answer = ""
        
    if build_tree_only:
        reasoning_tree = build_reasoning_tree(dataset_name, question, q_index, reasoner)
        return reasoning_tree, postorder_q_list, ""
    
    if execute_tree_only:
        reasoning_tree = input_tree
        if isinstance(reasoning_tree, str) and reasoning_tree == "TREE_PARSING_ERROR":
            print(f"\n### Tree parsing error for Question {q_index}: \"{question}\"") 
            print("Returning empty answers.")
            return reasoning_tree, None, ""
        postorder_q_list = convert_question_tree_to_list(reasoning_tree, question, q_index)
        predicted_answer, tree_clean, tree_full = execute_postorder_q_list(reasoner, dataset_name, reasoning_tree, postorder_q_list, q_index, gold) 
        
        return reasoning_tree, postorder_q_list, predicted_answer
 

### Function to evaluate jsonl dataset
def evaluate_dataset(reasoner: GlobalReasoner, dataset_name: str, dataset_path: Optional[str] = "", input_trees_path: Optional[str] = "", output_trees_path: Optional[str] = "", output_predictions_path: Optional[str] = "", build_trees_only: Optional[bool] = False, execute_trees_only: Optional[bool] = False):
    

    if (int(build_trees_only) + int(execute_trees_only)) != 1:
        raise Exception("Need to set exactly one mode to True: ['build_trees_only', 'execute_trees_only']")
    
    global num_llm_calls
    em = 0
    cover_em = 0
    f1 = 0.0
    num_entries = 0
    num_tree_parsing_failures = 0
    num_execution_failures = 0
    num_continuous_failed_executions = 0
    s = time.time()
    
    # Mode 1 - only build reasoning trees given dataset questions
    if build_trees_only:          
        with open(dataset_path, 'r', encoding='utf-8') as dataset:  # Load test entries
            entries = [json.loads(line) for line in dataset]

        temp_output_path = output_trees_path + '.tmp'  # Temporary file to store intermediate results (out of order due to concurrency)
        with open(temp_output_path, 'w', encoding='utf-8') as temp_output:  # Build trees
            with Pool(processes=NUM_PROCESSES) as pool:
                results = []
                pbar = tqdm(total=len(entries), desc="Building Reasoning Trees")
                
                def update_progress(result):
                    temp_output.write(json.dumps(result) + '\n')  # store cur result
                    temp_output.flush()
                    os.fsync(temp_output.fileno())
                    pbar.update(1)  # update the progress bar
                
                for entry in entries:
                    result = pool.apply_async(build_tree_concurrently, args=(dataset_name, entry, reasoner), callback=update_progress)
                    results.append(result)

                pool.close()
                pool.join() 
                pbar.close()

        with open(temp_output_path, 'r', encoding='utf-8') as temp_output:  # read temp results and sort them
            final_results = [json.loads(line) for line in temp_output]

        # Store final ordered results
        final_results.sort(key=lambda x: x["index"])  # sort by index
        with open(output_trees_path, 'w', encoding='utf-8') as output_trees:
            for result in final_results:
                reasoning_tree = result["reasoning_tree"]
                if isinstance(reasoning_tree, str) and reasoning_tree == "TREE_PARSING_ERROR":
                    num_tree_parsing_failures += 1
                output_trees.write(json.dumps(result) + '\n')

        os.remove(temp_output_path)  # Clean temporary file if ordered file successfully saved
        print("Total tree parsing failures:", num_tree_parsing_failures)
        return
    
    # Mode 2 - only execute pre-built reasoning trees
    if execute_trees_only:
        if input_trees_path is None:
            raise Exception("Error: 'execute_trees_only=True', but 'input_trees_path' is None")
        
        with open(input_trees_path, 'r', encoding='utf-8') as input_trees, \
            open(output_predictions_path, 'w', encoding='utf-8') as output_predictions:
            for line in input_trees:
                entry = json.loads(line)
                question = entry["question"].strip()
                question_index = entry["index"]
                gold_answers = entry["gold"]
                reasoning_tree = entry["reasoning_tree"]
                predicted_answer = ""  # set default empty value

                try: 
                    _, postorder_q_list, predicted_answer = run_query(reasoner=reasoner, dataset_name=dataset_name, question=question, q_index=question_index, gold=gold_answers, 
                                                 build_tree_only=build_trees_only, execute_tree_only=execute_trees_only, input_tree=reasoning_tree)
                    num_continuous_failed_executions = 0  # successful execution, refreshing failed_executions to 0
                except Exception as e:
                    print(f"\n!!! [Question execution failure] Question {question_index}: '{question}'")  # very small possibility, most probable for API retrieval errors
                    print("Exception:", e)
                    print("Traceback:", traceback.format_exc())
                    print("Storing empty predicted_answer.")
                    num_execution_failures += 1
                    num_continuous_failed_executions += 1
                    if num_continuous_failed_executions >= 3:
                        print("More than 3 execution failures in a row. Please check whether your APIs are working correctly. \nExiting.")
                        exit()
                
                if isinstance(reasoning_tree, str) and reasoning_tree == "TREE_PARSING_ERROR":
                    num_tree_parsing_failures += 1
                
                # Save prediction to file
                output_predictions.write(json.dumps({"index": question_index, "question": question, "predicted": predicted_answer, "gold": gold_answers}) + '\n')
                output_predictions.flush()
                os.fsync(output_predictions.fileno())
                
                # Update metrics
                cur_em, cur_cover_em = calculate_em(predicted_answer, gold_answers)
                cur_f1 = calculate_f1(predicted_answer, gold_answers)
                em += cur_em
                cover_em += cur_cover_em
                f1 += cur_f1
                
                print("Is Exact Match:", bool(cur_em))
                print("Is Cover EM:", bool(cur_cover_em))
                print("Cur F1:", cur_f1)
                
                num_entries += 1                
                if num_entries % 10 == 0:
                    print_results(em, cover_em, f1, num_entries, num_tree_parsing_failures, num_execution_failures, s)
                    
                # exit() # debug
                        
            print_results(em, cover_em, f1, num_entries, num_tree_parsing_failures, num_execution_failures, s)
            return


def evaluate_dataset_single_source(dataset_name, dataset_path, output_trees_path, output_predictions_path, text_retriever_url, llm_cache_path="../openai_service/llm_cache/cache.jsonl", k=3):
    
    dataset_name = dataset_name.lower().strip()
    if dataset_name not in {"hotpotqa", "2wikimultihop", "musique"}: 
        raise Exception(f"Unsupported single-source dataset: {dataset_name}. List of supported datasets: HotpotQA, 2WikiMultiHop, Musique.")
    
    knowledge_sources = {"Text"} 
    openai_caller = OpenAICaller(cache_path=llm_cache_path) 
    global_reasoner = GlobalReasoner(openai_caller=openai_caller, available_knowledge_sources=knowledge_sources, text_retriever_url=text_retriever_url, k=k)
    
    # Stage 1 - Atomic Reasoning Planning (Tree Generation)
    evaluate_dataset(reasoner=global_reasoner,
                     dataset_name=dataset_name,
                     dataset_path=dataset_path,
                     output_trees_path=output_trees_path, 
                     build_trees_only=True)
    
    # Stage 2 - Atomic Reasoning Execution (Tree Execution)
    evaluate_dataset(reasoner=global_reasoner,
                     dataset_name=dataset_name,
                     input_trees_path=output_trees_path, 
                     output_predictions_path=output_predictions_path, 
                     execute_trees_only=True)
    
    
def evaluate_dataset_multi_source(dataset_name, dataset_path, output_trees_path, output_predictions_path, text_retriever_url, google_serpapi_key, kopl_parser_url="https://viskop.xlore.cn/programApi", kopl_engine_url = "https://viskop.xlore.cn/large", llm_cache_path="../openai_service/llm_cache/cache.jsonl", k=3):
    
    dataset_name = dataset_name.lower().strip()
    if dataset_name not in {"blendqa", "crag"}: 
        raise Exception(f"Unsupported multi-source dataset: {dataset_name}. List of supported datasets: BlendQA, CRAG.")
    
    knowledge_sources = {"Text", "Web", "KB"}
    openai_caller = OpenAICaller(cache_path=llm_cache_path)
    global_reasoner = GlobalReasoner(openai_caller=openai_caller, available_knowledge_sources=knowledge_sources, text_retriever_url=text_retriever_url, 
                                    serpapi_key=google_serpapi_key, 
                                    kopl_parser_url=kopl_parser_url, kopl_engine_url=kopl_engine_url, 
                                    k=k)
    
    # Stage 1 - Atomic Reasoning Planning (Tree Generation)
    evaluate_dataset(reasoner=global_reasoner, 
                     dataset_name=dataset_name,
                     dataset_path=dataset_path, 
                     output_trees_path=output_trees_path, 
                     build_trees_only=True)
    
    # Stage 2 - Atomic Reasoning Execution (Tree Execution)
    evaluate_dataset(reasoner=global_reasoner, 
                     dataset_name=dataset_name,
                     input_trees_path=output_trees_path,
                     output_predictions_path=output_predictions_path, 
                     execute_trees_only=True)
     
     
if __name__ == "__main__":
    
    s = time.time()
    torch.multiprocessing.set_start_method('spawn')
    
    """ Adjust the following code to evaluate different datasets """
    
    ### Single-source example
    dataset_name = "HotpotQA"
    dataset_path = "../datasets/single_source/HotpotQA/hotpotqa_test_500.jsonl"
    output_trees_path = "../results/hotpotqa_test_500_trees.jsonl"
    output_predictions_path = "../results/hotpotqa_test_500_predictions.jsonl"
    text_retriever_url = "http://localhost:1212/api/search"  # HotpotQA wiki dump
    evaluate_dataset_single_source(dataset_name=dataset_name, dataset_path=dataset_path, output_trees_path=output_trees_path, output_predictions_path=output_predictions_path, text_retriever_url=text_retriever_url)
    
    ### Multi-source example
    dataset_name = "BlendQA"
    dataset_path = "../datasets/multi_source/BlendQA/kg-web_132.jsonl"
    output_trees_path = "../results/blendqa_kg-web_132_trees.jsonl"
    output_predictions_path = "../results/blendqa_kg-web_132_predictions.jsonl"
    text_retriever_url = "http://localhost:1214/api/search"  # Atlas wiki dump
    google_serpapi_key = "YOUR_SERPAPI_KEY"  # TODO: put your SERPAPI key
    evaluate_dataset_multi_source(dataset_name=dataset_name, dataset_path=dataset_path, output_trees_path=output_trees_path, output_predictions_path=output_predictions_path, text_retriever_url=text_retriever_url, google_serpapi_key=google_serpapi_key)
    