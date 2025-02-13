from typing import Optional
from collections import OrderedDict
import traceback

from knowledge_sources import Text, Web, KB
from query_knowledge_source.query_llm import OpenAICaller
from prompts.answer_formulation_prompts import format_direct_rag_prompt_hotpotqa, format_relate_prompt_hotpotqa, format_filter_prompt_hotpotqa, format_search_prompt_hotpotqa, format_answer_from_child_qa_pairs_prompt_hotpotqa, format_direct_answer_prompt_hotpotqa
from prompts.answer_formulation_prompts import format_direct_rag_prompt_2wiki, format_relate_prompt_2wiki, format_filter_prompt_2wiki, format_search_prompt_2wiki, format_answer_from_child_qa_pairs_prompt_2wiki, format_direct_answer_prompt_2wiki
from prompts.answer_formulation_prompts import format_direct_rag_prompt_musique, format_relate_prompt_musique, format_filter_prompt_musique, format_search_prompt_musique, format_answer_from_child_qa_pairs_prompt_musique, format_direct_answer_prompt_musique
from prompts.answer_formulation_prompts import format_direct_rag_prompt_blendqa, format_relate_prompt_blendqa, format_filter_prompt_blendqa, format_search_prompt_blendqa, format_answer_from_child_qa_pairs_prompt_blendqa, format_direct_answer_prompt_blendqa
from utils import extract_llm_answers
from prompts.answer_formulation_prompts import format_direct_rag_prompt_crag, format_relate_prompt_crag, format_filter_prompt_crag, format_search_prompt_crag, format_answer_from_child_qa_pairs_prompt_crag, format_direct_answer_prompt_crag


### Prompt mappings

direct_rag_prompts = {
    'hotpotqa': format_direct_rag_prompt_hotpotqa,
    '2wikimultihop': format_direct_rag_prompt_2wiki,
    'musique': format_direct_rag_prompt_musique,
    'blendqa': format_direct_rag_prompt_blendqa,
    'crag': format_direct_rag_prompt_crag
}

direct_answer_prompts = {
    'hotpotqa': format_direct_answer_prompt_hotpotqa,
    '2wikimultihop': format_direct_answer_prompt_2wiki,
    'musique': format_direct_answer_prompt_musique,
    'blendqa': format_direct_answer_prompt_blendqa,
    'crag': format_direct_answer_prompt_crag
}

search_prompts = {
    'hotpotqa': format_search_prompt_hotpotqa,
    '2wikimultihop': format_search_prompt_2wiki,
    'musique': format_search_prompt_musique,
    'blendqa': format_search_prompt_blendqa,
    'crag': format_search_prompt_crag
}

relate_prompts = {
    'hotpotqa': format_relate_prompt_hotpotqa,
    '2wikimultihop': format_relate_prompt_2wiki,
    'musique': format_relate_prompt_musique,
    'blendqa': format_relate_prompt_blendqa,
    'crag': format_relate_prompt_crag
}

filter_prompts = {
    'hotpotqa': format_filter_prompt_hotpotqa,
    '2wikimultihop': format_filter_prompt_2wiki,
    'musique': format_filter_prompt_musique,
    'blendqa': format_filter_prompt_blendqa,
    'crag': format_filter_prompt_crag
}

answer_from_child_qa_prompts = {
    'hotpotqa': format_answer_from_child_qa_pairs_prompt_hotpotqa,
    '2wikimultihop': format_answer_from_child_qa_pairs_prompt_2wiki,
    'musique': format_answer_from_child_qa_pairs_prompt_musique,
    'blendqa': format_answer_from_child_qa_pairs_prompt_blendqa,
    'crag': format_answer_from_child_qa_pairs_prompt_crag
}


### Util Functions

def format_text_retrieval_answers(full_answers):
    return ' ... '.join(f"[{entry['rank']}] {entry['entity']} | {entry['passage']}" for entry in full_answers)


def format_web_retrieval_answers(full_answers, k, print_article_text=True):
    result_index = 1
    
    str_results_list = []
    for result_type, result in full_answers.items():
        if result_type != "organic_results":  # answer_box or knowledge_graph results, single dict
            title = ""
            contents = []
            for attribute, value in result.items():
                if value != "":  # only add non-empty knowledge fields
                    if attribute == "title":
                        title = f"{value} | "
                    if attribute == "snippet":
                        contents.append(value)
                    if attribute == "article_text" and print_article_text:
                        contents.append(value)
            str_result = ""
            if len(title) > 0:
                str_result += title
            if len(contents) > 0:
                str_result += " ".join(contents)
            if len(str_result) > 0:  # only add if non-empty
                str_results_list.append(f"[{str(result_index)}] {str_result}".strip())
                result_index += 1
        else:  # organic_results, list of dic
            organic_results = result
            for organic_result in organic_results:
                if result_index > k:  # only take top k results, including non-organic and organic
                    break
                title = ""
                contents = []
                for attribute, value in organic_result.items():
                    if value != "":  # only add non-empty knowledge fields
                        if attribute == "title":
                            title = f"{value} | "
                        if attribute == "snippet":
                            contents.append(value)
                        if attribute == "article_text" and print_article_text:
                            contents.append(value)
                str_result = ""
                if len(title) > 0:
                    str_result += title
                if len(contents) > 0:
                    str_result += " ".join(contents)
                if len(str_result) > 0:  # only add if non-empty
                    # print("organic result_index:", result_index)
                    str_results_list.append(f"[{str(result_index)}] {str_result}".strip())
                    result_index += 1
   
    concatenated_str_ans = (" ".join(str_results_list)).strip()
    return concatenated_str_ans


def format_kb_retrieval_answers(clean_answers):
    return ", ".join(clean_answers)


### Debug functions

def print_supporting_knowledge(supporting_knowledge):
    knowledge = ""
    if "Text" in supporting_knowledge:
        if len(supporting_knowledge['Text']) > 0:
            knowledge += f"\nWikipedia Passages: {supporting_knowledge['Text']}"
    if "Web" in supporting_knowledge:
        if len(supporting_knowledge) > 0:
            knowledge += f"\nGoogle Results: {supporting_knowledge['Web']}"
    if "KB" in supporting_knowledge:
        if len(supporting_knowledge) > 0:
            knowledge += f"\nWikidata Query Results: {supporting_knowledge['KB']}"
        
    print("=== Supporting knowledge: ")
    print(knowledge)


### GlobalReasoner Class

class GlobalReasoner:
    def __init__(self, openai_caller: OpenAICaller, available_knowledge_sources: set, text_retriever_url: Optional[str] = None, serpapi_key: Optional[str] = None, kb_query_language: Optional[str] = "KoPL", kopl_parser_url: Optional[str] = None, kopl_engine_url: Optional[str] = None, k: Optional[int] = 3):
        
        if len(available_knowledge_sources) == 0:
            raise Exception("len(available_knowledge_sources) == 0: please provide at least one knowledge source in [Text, Web, KB].")
        if text_retriever_url is None and serpapi_key is None and kb_query_language is None:
            raise Exception("All API urls None: please provide at least one parameter in [text_retriever_url, serpapi_key, kb_query_language].")

        self.openai_caller = openai_caller
        
        self.available_knowledge_sources = available_knowledge_sources
        if "Text" in available_knowledge_sources:
            self.text = Text(text_retriever_url, k)
            self.k = k
        if "Web" in available_knowledge_sources:
            self.web = Web(serpapi_key, k)
            self.k = k
        if "KB" in available_knowledge_sources:
            self.kb = KB(kb_query_language, kopl_parser_url, kopl_engine_url)
            
        print(f"GlobalReasoner instance initialized. Available Knowledge Sources = {available_knowledge_sources}.")


    def direct_Answer(self, dataset_name, question: str):
        prompt = direct_answer_prompts[dataset_name](question)
            
        llm_response, finish_reason = self.openai_caller.query_gpt4o(prompt=prompt, max_tokens=256)
        if finish_reason == "length": 
            llm_response, finish_reason = self.openai_caller.query_gpt4o(prompt=prompt, max_tokens=512)
            print("direct_Answer() finish_reason = \"length\", reran with max_tokens=512.")
        
        print("llm_response:", llm_response)  # debug
        paraphrase_answer, clean_answer_list = extract_llm_answers(llm_response)
            
        return clean_answer_list, paraphrase_answer
        
        
    def direct_RAG(self, dataset_name: str, knowledge_sources: set, question: str):
        supporting_knowledge = {}
        
        for knowledge_source in knowledge_sources:
            retrieved_knowledge = ""  # initialize for each round
            if knowledge_source == "Text": 
                clean_titles, full_answers = self.text.retrieve_topk_passages(question, self.text.k)
                if full_answers is not None:
                    retrieved_knowledge = format_text_retrieval_answers(full_answers)
            elif knowledge_source == "Web": 
                clean_titles, full_answers = self.web.retrieve_topk_articles(question, self.web.k)  # directly returns full article_text instead of functions' top related passage
                if full_answers is not None:
                    retrieved_knowledge = format_web_retrieval_answers(full_answers, self.web.k, print_article_text=False)  # only provide web article snippets for direct_RAG
            elif knowledge_source == "KB":
                clean_answers, full_answers = self.kb.obtain_kopl_results(question)
                if clean_answers is not None:  # note that for KB full_answers may be none, but it doesn't matter as long as clean_answers is not None
                    retrieved_knowledge = format_kb_retrieval_answers(clean_answers)
            
            if len(retrieved_knowledge) > 0:
                supporting_knowledge[knowledge_source] = retrieved_knowledge
            
        print_supporting_knowledge(supporting_knowledge)  # debug
        
        prompt = direct_rag_prompts[dataset_name](question, supporting_knowledge)
            
        llm_response, finish_reason = self.openai_caller.query_gpt4o(prompt=prompt, max_tokens=256)
        if finish_reason == "length": 
            llm_response, finish_reason = self.openai_caller.query_gpt4o(prompt=prompt, max_tokens=512)
            print("direct_RAG() finish_reason = \"length\", reran with max_tokens=512.")
        
        print("llm_response:", llm_response)  # debug
            
        # For text and search engine retrieval, only allow up to 2k answers to avoid exponential search space
        # if "Text" in knowledge_sources or "Web" in knowledge_sources:
        #     if len(clean_answer_list > 2 * self.k):
        #         clean_answer_list = clean_answer_list[:2*self.k]
        
        paraphrase_answer, clean_answer_list = extract_llm_answers(llm_response)
            
        return clean_answer_list, paraphrase_answer, supporting_knowledge
        
        
    def Search(self, dataset_name: str, knowledge_sources: set, question: str, entity_name: str, descriptors: Optional[str] = ""):
        supporting_knowledge = {}
        
        for knowledge_source in knowledge_sources:
            if knowledge_source == "Text": 
                clean_answers, full_answers = self.text.Search(question, entity_name, descriptors)
                if full_answers is not None:
                    supporting_knowledge["Text"] = format_text_retrieval_answers(full_answers)
                print("text.Search() done.")
            elif knowledge_source == "Web": 
                clean_titles, full_answers = self.web.Search(question, entity_name, descriptors)
                if full_answers is not None:
                    supporting_knowledge["Web"] = format_web_retrieval_answers(full_answers, self.web.k, print_article_text=False)
                print("web.Search() done.")
            elif knowledge_source == "KB":
                clean_answers, full_answers = self.kb.Search(question, entity_name, descriptors)
                supporting_knowledge["KB"] = format_kb_retrieval_answers(clean_answers)  # KB's search function never returns None, no need to check
                print("kb.Search() done.")
        
        if supporting_knowledge == {}:
            raise Exception("Search() function execution failed: obtained empty supporting knowledge.")
        
        print_supporting_knowledge(supporting_knowledge)  # debug
        
        if descriptors != "":  # add descriptors to question
            question = f"{question} ({descriptors})"
            
        prompt = search_prompts[dataset_name](question, supporting_knowledge)
            
        llm_response, finish_reason = self.openai_caller.query_gpt4o(prompt=prompt, max_tokens=256)
        if finish_reason == "length": 
            llm_response, finish_reason = self.openai_caller.query_gpt4o(prompt=prompt, max_tokens=512)
            print("Search() finish_reason = \"length\", reran with max_tokens=512.")
        
        print("llm_response:", llm_response)  # debug
        
        paraphrase_answer, clean_answer_list = extract_llm_answers(llm_response)
            
        return clean_answer_list, paraphrase_answer, supporting_knowledge
        
        
    def Relate(self, dataset_name: str, knowledge_sources: set, question: str, entity: str, relation: str):
        supporting_knowledge = {}
        
        for knowledge_source in knowledge_sources:
            if knowledge_source == "Text": 
                clean_answers, full_answers = self.text.Relate(question, entity, relation)
                if clean_answers is not None and full_answers is not None:
                    supporting_knowledge["Text"] = format_text_retrieval_answers(full_answers)
            elif knowledge_source == "Web": 
                clean_titles, full_answers = self.web.Relate(question, entity, relation)
                if full_answers is not None:
                    supporting_knowledge["Web"] = format_web_retrieval_answers(full_answers, k=self.web.k, print_article_text=False)
            elif knowledge_source == "KB":
                clean_answers, full_answers = self.kb.Relate(question, entity, relation)
                if clean_answers is not None:
                    supporting_knowledge["KB"] = format_kb_retrieval_answers(clean_answers)
        
        if supporting_knowledge == {}:
            raise Exception("Relate() function execution failed: obtained empty supporting knowledge.")
        
        print_supporting_knowledge(supporting_knowledge)  # debug
        
        prompt = relate_prompts[dataset_name](question, supporting_knowledge)
        
        llm_response, finish_reason = self.openai_caller.query_gpt4o(prompt=prompt, max_tokens=256)  
        if finish_reason == "length": 
            llm_response, finish_reason = self.openai_caller.query_gpt4o(prompt=prompt, max_tokens=512)
            print("Relate() finish_reason = \"length\", reran with max_tokens=512.")
            
        print("llm_response:", llm_response)  # debug
        
        paraphrase_answer, clean_answer_list = extract_llm_answers(llm_response)
            
        return clean_answer_list, paraphrase_answer, supporting_knowledge        
    
        
    def Filter(self, dataset_name: str, knowledge_sources: set, question: str, entities: list, condition: str):
        supporting_knowledge = {}
        
        for knowledge_source in knowledge_sources:
            if knowledge_source == "Text": 
                clean_answers, full_answers = self.text.Filter(question, entities, condition)
                if full_answers is not None:
                    supporting_knowledge["Text"] = format_text_retrieval_answers(full_answers)
            elif knowledge_source == "Web":
                clean_answers, full_answer_results_dict = self.web.Filter(question, entities, condition)
                if full_answer_results_dict is not None:  # note: need to loop through each kv pair
                    filter_string_answer = ""
                    for entity, results in full_answer_results_dict.items():
                        filter_string_answer += f"'{entity}' related results: \n"
                        filter_string_answer += format_web_retrieval_answers(results, k=self.web.k, print_article_text=False)
                    supporting_knowledge["Web"] = filter_string_answer
            elif knowledge_source == "KB":
                clean_answers, full_answers = self.kb.Filter(question, entities, condition)
                if clean_answers is not None:
                    supporting_knowledge["KB"] = format_kb_retrieval_answers(clean_answers)
        
        if supporting_knowledge == {}:
            raise Exception("Filter() function execution failed: obtained empty supporting knowledge.")
        
        print_supporting_knowledge(supporting_knowledge)  # debug
        
        prompt = filter_prompts[dataset_name](question, condition, supporting_knowledge)
            
        llm_response, finish_reason = self.openai_caller.query_gpt4o(prompt=prompt, max_tokens=256)
        if finish_reason == "length": 
            llm_response, finish_reason = self.openai_caller.query_gpt4o(prompt=prompt, max_tokens=512)
            print("Filter() finish_reason = \"length\", reran with max_tokens=512.")
        
        print("llm_response:", llm_response)  # debug
        
        paraphrase_answer, clean_answer_list = extract_llm_answers(llm_response)
            
        return clean_answer_list, paraphrase_answer, supporting_knowledge
    
    
    def AnswerFromQAPairs(self, dataset_name: str, question: str, child_qa_pairs: str):  # moved from main.py to here
        
        prompt = answer_from_child_qa_prompts[dataset_name](question, child_qa_pairs)
            
        llm_response, finish_reason = self.openai_caller.query_gpt4o(prompt=prompt, max_tokens=256)
        if finish_reason == "length": 
            llm_response, finish_reason = self.openai_caller.query_gpt4o(prompt=prompt, max_tokens=512)
            print("AnswerFromQAPairs() finish_reason = \"length\", reran with max_tokens=512.")
        
        print("llm_response:", llm_response)  # debug
        
        paraphrase_answer, clean_answer_list = extract_llm_answers(llm_response)        
        supporting_knowledge = {"child_qa_pairs": child_qa_pairs}

        return clean_answer_list, paraphrase_answer, supporting_knowledge
        