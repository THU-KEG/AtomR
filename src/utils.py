import json
import re
import ast
import os


def extract_json_tree(text):
    def remove_inner_ending_quotes(text):  # i.e. "When was the word Slavs" used"
        pattern = r'(?<=[a-zA-Z])"([^"]*?)"(?=[\n,:}\]])'  # matches starting with a quote after a letter and ending with a quote before a newline, comma, :, }, or ]
    
        def replace_match(match):
            return match.group(0)[1:]  # remove the first character, which is the starting quote
        
        fixed_text = re.sub(pattern, replace_match, text)  # replace all matches
        
        return fixed_text
    
    def remove_inner_starting_quotes(text):   # i.e. "When was the word "Slavs used"
        pattern = r'(?<!\\)(?<=[ \n,:[{])("[^"\\]*(?<!\\)")(?![\n,:}\]])'
        matches = list(re.finditer(pattern, text, re.MULTILINE))  # matches starting with a quote not after a newline, comma, :, }, or ], and ending with one before a newline, comma, :, }, or ]
        
        if not matches:
            return text
        
        fixed_text = text
        offset = 0  # offset to handle the change in string length after modifications
        for match in matches:
            start, end = match.span()
            start_adjusted = start + offset
            end_adjusted = end + offset
            fixed_text = fixed_text[:end_adjusted-1] + fixed_text[end_adjusted:] # remove the right quotation mark
            offset -= 1  # adjust offset for each quote removed

        return fixed_text
    
    def find_parentheses_substrings(s):
        stack = []
        results = []
        start = None
        
        for i, char in enumerate(s):
            if char == '(':
                if start is None:
                    start = i  # Mark the start of the outermost parenthesis
                stack.append(i)
            elif char == ')':
                stack.pop()
                if not stack:  # No more open parentheses
                    results.append((start, i + 1))  # Store the start and end positions of the matched substring
                    start = None
        
        return results

    def format_function_quotes(match):  # format quotation marks of leaf functions
        # text = match.group(0)
        text = match
        text = re.sub(r'(?<!\\)"', r'\\"', text)  # change all " to \"
        pattern = r"(?<=[(, ])'|'(?=[,)])"  # replace ' with \" only if it encloses a parameter (avoiding i.e. men's)
        text = re.sub(pattern, '\\"', text)  
        text = re.sub(r"\\'", "'", text)  # \' will lead to errors, changing to '
        return text
        
        # modified_content = match.group(0).replace('"', '\\"')
        # modified_content = modified_content.replace("\\'", "'")
        # return modified_content
    
    # locate JSON string from LLM response
    start_index = text.find('{')
    end_index = text.rfind('}')
    json_tree_str = text[start_index:end_index + 1]
    
    # try 1
    try:
        json_tree = json.loads(json_tree_str)
    except Exception as e:
        print("!!! Original tree parsing failed.")
        print("Error: ", e)
        print("Postprocessing JSON string and trying again.")
        
    # postprocess JSON string punctuation
    ### format keys and values
    json_tree_str = json_tree_str.replace("{'", '{"')  
    json_tree_str = json_tree_str.replace("'}", '"}')
    json_tree_str = json_tree_str.replace("['", '["')
    json_tree_str = json_tree_str.replace("']", '"]')
    json_tree_str = json_tree_str.replace("', ", '", ')
    json_tree_str = json_tree_str.replace(", '", ', "')
    json_tree_str = json_tree_str.replace("': ", '": ')
    json_tree_str = json_tree_str.replace("' :", '" :')
    json_tree_str = json_tree_str.replace(": '", ': "')
    json_tree_str = json_tree_str.replace(":'", ':"')
    json_tree_str = json_tree_str.replace("\n'", '\n"')
    json_tree_str = json_tree_str.replace("'\n", '"\n')
    json_tree_str = json_tree_str.replace("\t'", '\t"')
    json_tree_str = json_tree_str.replace("'[END]", '"[END]')
    json_tree_str = json_tree_str.replace("[END]'", '[END]"')
    json_tree_str = re.sub(r"'(\d+\.)", r'"\1', json_tree_str)  # format question indices
    ### format leaf atomic functions
    json_tree_str = json_tree_str.replace("'Search(", '"Search(')
    json_tree_str = json_tree_str.replace("'Filter(", '"Filter(')
    json_tree_str = json_tree_str.replace("'Relate(", '"Relate(')
    json_tree_str = json_tree_str.replace("'Intersection(", '"Intersection(')
    json_tree_str = re.sub(r"\)'(?![a-zA-Z])", ')"', json_tree_str)  # replace )' with )" only if the right is not an alphabetical letter
    # json_tree_str = re.sub(r'\([^)]*\)', format_function_quotes, json_tree_str)
    par_substrings = find_parentheses_substrings(json_tree_str)
    for start, end in reversed(par_substrings):
        original_substring = json_tree_str[start:end]
        modified_substring = format_function_quotes(original_substring)
        json_tree_str = json_tree_str[:start] + modified_substring + json_tree_str[end:]
    ### remove extra inner quotes
    json_tree_str = remove_inner_starting_quotes(json_tree_str)  # i.e. hotpotqa dev question idx 33
    json_tree_str = remove_inner_ending_quotes(json_tree_str)
    ### replace invalid \' escapes
    json_tree_str = json_tree_str.replace("\\'", "'")  
    
    # # postprocess JSON string punctuation
    # if '":' in json_tree_str and '",' in json_tree_str:  # some keys and attributes already enclosed in "
    #     # format leaf atomic function parameters
    #     json_tree_str = json_tree_str.replace("'Search(", '"Search(')
    #     json_tree_str = json_tree_str.replace("'Filter(", '"Filter(')
    #     json_tree_str = json_tree_str.replace("'Relate(", '"Relate(')
    #     json_tree_str = json_tree_str.replace("'Intersection(", '"Intersection(')
    #     json_tree_str = re.sub(r"\)'(?![a-zA-Z])", ')"', json_tree_str)  # replace )' with )" only if the right is not an alphabetical letter
    #     # json_tree_str = re.sub(r'\([^)]*\)', format_function_quotes, json_tree_str)
    #     par_substrings = find_parentheses_substrings(json_tree_str)
    #     for start, end in reversed(par_substrings):
    #         original_substring = json_tree_str[start:end]
    #         modified_substring = format_function_quotes(original_substring)
    #         json_tree_str = json_tree_str[:start] + modified_substring + json_tree_str[end:]
    #     json_tree_str = json_tree_str.replace("{'", '{"')  
    #     json_tree_str = json_tree_str.replace("'}", '"}')
    #     json_tree_str = json_tree_str.replace("['", '["')
    #     json_tree_str = json_tree_str.replace("']", '"]')
    #     json_tree_str = json_tree_str.replace("', ", '", ')
    #     json_tree_str = json_tree_str.replace(", '", ', "')
    #     json_tree_str = json_tree_str.replace("': ", '": ')
    #     json_tree_str = json_tree_str.replace(": '", ': "')
    #     json_tree_str = json_tree_str.replace("\n'", '\n"')
    #     json_tree_str = json_tree_str.replace("'\n", '"\n')
    #     json_tree_str = json_tree_str.replace("\t'", '\t"')
    #     json_tree_str = remove_inner_starting_quotes(json_tree_str)  # i.e. hotpotqa dev question idx 33
    #     json_tree_str = remove_inner_ending_quotes(json_tree_str)
    #     json_tree_str = json_tree_str.replace("'[END]", '"[END]')
    #     json_tree_str = json_tree_str.replace("[END]'", '[END]"')
    #     json_tree_str = re.sub(r"'(\d+\.)", r'"\1', json_tree_str)  # format question indices
    #     json_tree_str = json_tree_str.replace("\\'", "'")  # replace invalid ' escapes
    # else:  # all keys and attributes enclosed in '
    #     json_tree_str = json_tree_str.replace('"', '\\"')  # replace existing " with \"
    #     json_tree_str = json_tree_str.replace("{'", '{"')  # replace entry enclosing ' with "
    #     json_tree_str = json_tree_str.replace("'}", '"}')
    #     json_tree_str = json_tree_str.replace("['", '["')
    #     json_tree_str = json_tree_str.replace("']", '"]')
    #     json_tree_str = json_tree_str.replace("', ", '", ')
    #     json_tree_str = json_tree_str.replace(", '", ', "')
    #     json_tree_str = json_tree_str.replace("': ", '": ')
    #     json_tree_str = json_tree_str.replace(": '", ': "')
    #     json_tree_str = json_tree_str.replace("\n'", '\n"')
    #     json_tree_str = json_tree_str.replace("'\n", '"\n')
    #     json_tree_str = json_tree_str.replace("\t'", '\t"')
    #     json_tree_str = json_tree_str.replace("'Search(", '"Search(')
    #     json_tree_str = json_tree_str.replace("'Filter(", '"Filter(')
    #     json_tree_str = json_tree_str.replace("'Relate(", '"Relate(')
    #     json_tree_str = json_tree_str.replace("'Intersection(", '"Intersection(')
    #     json_tree_str = re.sub(r"\)'(?![a-zA-Z])", ')"', json_tree_str)  # replace )' with )" only if the right is not an alphabetical letter
    #     # json_tree_str = re.sub(r'\([^)]*\)', format_function_quotes, json_tree_str)
    #     par_substrings = find_parentheses_substrings(json_tree_str)
    #     for start, end in reversed(par_substrings):
    #         original_substring = json_tree_str[start:end]
    #         modified_substring = format_function_quotes(original_substring)
    #         json_tree_str = json_tree_str[:start] + modified_substring + json_tree_str[end:]
    #     json_tree_str = json_tree_str.replace("'[END]", '"[END]')
    #     json_tree_str = json_tree_str.replace("[END]'", '[END]"')
    #     json_tree_str = re.sub(r"'(\d+\.)", r'"\1', json_tree_str)  # format question indices
    #     json_tree_str = json_tree_str.replace("\\'", "'")  # replace invalid ' escapes
    
    # try 2
    try:
        json_tree = json.loads(json_tree_str)
    except Exception as e:
        with open("debug/json_tree_str.txt", 'w') as file:  # write json_tree_str to debug file
            file.write(json_tree_str)
            file.flush()
        raise e
        
    return json_tree


def extract_function_parameters(function_str):
    
    left_par_idx = function_str.find('(')
    right_par_idx = function_str.rfind(')')

    try:
        params_str = function_str[left_par_idx + 1:right_par_idx]  # extract parameters inside outermost (), not including parentheses
        params = eval(f"({params_str},)")    # turn string into a tuple of parameters
        params = tuple(str(item) for item in params)  # make sure ref indices are parsed as strings, not lists
        return params
    except Exception as e:
        raise Exception("!!! [Error parsing function string]:", function_str)
        
    # pattern = r'\w+\((.*?)\)'  # old version, doesn't support in-parameter parenthesis
    # match = re.search(pattern, function_str)
    
    # if match:
    #     params_str = match.group(1)
    #     try:
    #         params = eval(f"({params_str},)")    # turn string into a tuple of parameters
    #         params = tuple(str(item) for item in params)  # make sure ref indices are parsed as strings, not lists
    #         return params
    #     except Exception as e:
    #         print("!!! [Error parsing function string]:", function_str)
    #         print("Error:", e)
    #         # exit()
    # else:
    #     raise Exception("!!! [Error parsing function string]:", function_str)
        

def extract_ref_indices(text):  
    pattern = r'\[\d+\]'
    matches = re.findall(pattern, text)
    
    if len(matches) == 0:
        return []
    
    return list(dict.fromkeys(matches))  # deduplicate


def find_qa_pairs_given_ref_indices(ref_indices, question_answer_dict):
    if len(ref_indices) == 0:
        return None, None
    
    # print("(entered find_qa_pairs_given_ref_indices())")  # debug
    
    ref_qa_pairs_list = {}
    ref_qa_pairs_paraphrase = {}
    
    answered_questions = list(question_answer_dict.keys())[:-1]  # pop last question (which is the current unanswered question)
    index_question_dict = {}
    
    # print("answered_questions:", answered_questions)  # debug
    
    for question in answered_questions:
        match = re.search(r'\d+', question)
        if match: 
            index = int(match.group(0))
            index_question_dict[f"[{str(index)}]"] = question
        
    for ref in ref_indices:
        q = index_question_dict[ref]
        # ans_list = question_answer_dict[q]  
        
        ans_list = []
        ans_paraphrase = ""
        ans_list =  question_answer_dict[q]["clean_answer_list"]  
        ans_paraphrase = question_answer_dict[q]["paraphrase_answer"]
            
        # for cur_ans_list in ans_dict.values():  # combine answer lists for each cue
        #     ans_list += cur_ans_list
        
        ref_qa_pairs_list[ref] = {"question": q, "answers": ans_list}  # pure answer list with no cue information
        ref_qa_pairs_paraphrase[ref] = {"question": q, "answers": ans_paraphrase}  # answer dict with cue information
        
    # print("ref_qa_pairs_paraphrase:", ref_qa_pairs_paraphrase)  # debug
    # print("ref_qa_pairs_list:", ref_qa_pairs_list)
    
    # return ref_qa_pairs
    return ref_qa_pairs_list, ref_qa_pairs_paraphrase


def extract_knowledge_sources(text, available_knowledge_sources):
    normalized_response = text.lower()
    chosen_sources = [source for source in {"Wikipedia", "Google", "Wikidata"} if source.lower() in normalized_response]
    chosen_source_to_knowledge_source_dict = {"Wikipedia": "Text", "Google": "Web", "Wikidata": "KB"}
    mapped_knowledge_sources = [chosen_source_to_knowledge_source_dict[source] for source in chosen_sources]
    
    if len(chosen_sources) == 0:  # if no knowledge source selected, return all available knowledge sources
        return available_knowledge_sources
    
    mapped_knowledge_sources = set(mapped_knowledge_sources)  # use set for quicker key access
    
    return mapped_knowledge_sources.intersection(available_knowledge_sources)


def extract_llm_answers(llm_response: str):  # with v6 paraphrase answers update
    match = re.search(r"answer is: (.*)", llm_response, re.IGNORECASE | re.DOTALL)  # match till end of string
    if match:
        ans = match.group(1)
    else:
        ans = llm_response

    # (1) Extract Paraphrase Answer
    extracted_paraphrase_answer = False
    paraphrase_answer = ans  # initialize value
    try:
        pattern = r'Paraphrase Answer:\s*(.*?)\s*(?=; \(2\) Answer List|\n\(2\) Answer List|\(2\) |Answer List)'
        match = re.search(pattern, paraphrase_answer)
        paraphrase_answer = match.group(1).strip()
        if paraphrase_answer[-1] == ';':
            paraphrase_answer = paraphrase_answer[:-1]
        extracted_paraphrase_answer = True
    except:
        print(f"!!! LLM Paraphrase Answer extraction failed. Returning paraphrase_answer={paraphrase_answer}")
    
    # (2) Extract clean Answer List
    ans = ans.replace(", ...", "")  # get rid of possible list ellipses
    ans = ans.replace(",...", "")
    list_index_s = ans.rfind('[')  # find last [
    list_index_e = ans.rfind(']')  # find last ]
    
    try:  # initialize value
        clean_answer_list = [ans[list_index_s:list_index_e + 1]] 
    except:
        clean_answer_list = [ans]
        
    try:
        clean_answer_list = ast.literal_eval(ans[list_index_s:list_index_e + 1])
    except:
        if extracted_paraphrase_answer:
            clean_answer_list = [paraphrase_answer]
            print(f"!!! LLM Answer List extraction failed. Returning clean_answer_list=[paraphrase_answer]")
        else:
            clean_answer_list = [ans]
            print(f"!!! LLM Answer List extraction failed. Returning clean_answer_list=[ans]")
    
    # Ensure all entries are in string type
    for i in range(len(clean_answer_list)):
        clean_answer_list[i] = str(clean_answer_list[i])
        
    return paraphrase_answer, clean_answer_list


# def extract_llm_answer_list(llm_response: str):
#     match = re.search(r"answer is: (.*)", llm_response, re.IGNORECASE)
#     if match:
#         ans = match.group(1)
#     else:
#         ans = llm_response
       
#     # get rid of possible list ellipses
#     ans = ans.replace(", ...", "")
#     ans = ans.replace(",...", "")
     
#     # extract list
#     list_index_s = ans.rfind('[')  # find last [
#     list_index_e = ans.rfind(']')  # find last ]
        
#     try:
#         ans_list = ast.literal_eval(ans[list_index_s:list_index_e + 1])
#         return ans_list
#     except:
#         return [ans]  # return original response if list extraction failed
    

if __name__ == "__main__":
    parameters = extract_function_parameters('Search([1], "creek")')
    print(parameters)
    print(type(parameters))
    print(len(parameters))
    print(parameters[0])
    