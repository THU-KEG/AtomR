from serpapi import GoogleSearch
import requests
import pandas as pd
from bs4 import BeautifulSoup
import re
import os


""" Helper functions """

def remove_citations(text):
    pattern = r'\[\d+\]'
    cleaned_text = re.sub(pattern, ' ', text)
    
    return cleaned_text


def remove_pre_p_entries(data):
    while True:
        if data[0]['label'] == 'p':
            break
        
        data.pop(0)
        
    return data


""" HTML Parsing Functions """

def parse_wikipedia_article(link):
    
    """ Process Text """
    
    response = requests.get(link)
    response.raise_for_status()  # will raise an exception for HTTP error codes

    wikipedia_text = response.text
    soup = BeautifulSoup(wikipedia_text, features="html.parser")
    article_blocks = []
    article_text = ""

    # Article text pre-processing
    for tag in soup.find_all(['h2', 'h3', 'h4', 'h5', 'h6', 'p', 'li']):  
        label = tag.name
        id = tag.get('id')
        content = tag.get_text(strip=True)
        
        if len(content) == 0:  # skip empty entries
            continue
        
        content = remove_citations(content)
        entry = {
            'label': label,
            'id': id,
            'content': content
        }
        article_blocks.append(entry)
        
    article_blocks = remove_pre_p_entries(article_blocks)  # Remove entries before the first paragraph
    
    for block in article_blocks:
        # Exclude excessive info at the end of the article
        if block['label'] == 'h2' and block['id'] == 'References':  
            break
        if block['id'] is not None and 'footer-info' in block['id']:  
            break
        
        # Parse content
        if block['label'] in {'h2', 'h3', 'h4', 'h5', 'h6'}:
            article_text += "\n\n" + block['content']
        elif block['label'] == "li":
            article_text += "\n- " + block['content']
        else:
            # article_text += block['content'] + " "
            article_text += "\n" + block['content']
        
    return article_text
    
    
def parse_other_article(link):
    try:
        response = requests.get(link)
        response.raise_for_status()  # will raise an exception for HTTP error codes
        
        soup = BeautifulSoup(response.content, 'html.parser')
        article_text = soup.get_text(separator=' ', strip=True)
        
    except Exception as e:
        print(f"Article Parse failed: {link}")
        print(f"Error: {e}")
        return None
    
    return article_text


""" Execute web query """

def execute_web_query(query, serpapi_key, k):
    params = {
    "api_key": serpapi_key,
    "engine": "google",
    "q": query,
    "location": "Austin, Texas, United States",
    "google_domain": "google.com",
    "gl": "us",
    "hl": "en"
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    clean_title_list = []  # stores article titles
    full_results = {}
    
    if "answer_box" in results:
        # Set default values
        answer_box_result = {}
        answer_box_result["rank"] = "Answer Box Result"
        answer_box_result["title"] = ""
        answer_box_result["snippet"] = ""
        answer_box_result["source"] = ""
        answer_box_result["link"] = ""
        answer_box_result["article_text"] = ""  # answer_box results always have article_text empty
        
        answer_box = results["answer_box"]
        if "answer" in answer_box:
            answer_box_result["title"] = answer_box["answer"]
            clean_title_list.append(answer_box_result["title"])
        if "snippet_highlighted_words" in answer_box and answer_box_result["title"] == "":
            answer_box_result["title"] = "; ".join(answer_box["snippet_highlighted_words"])
            clean_title_list.append(answer_box_result["title"])
        if "expanded_list" in answer_box and answer_box_result["title"] == "":
            answer_box_result["title"] = ", ".join(entry["title"] for entry in answer_box["expanded_list"])
            clean_title_list.append(answer_box_result["title"])
        if "snippet" in answer_box:
            answer_box_result["snippet"] = answer_box["snippet"]
        if "contents" in answer_box:
            if "formatted" in answer_box["contents"]:
                answer_box_result["snippet"] += " ... " + str(answer_box["contents"]["formatted"])
        if "list" in answer_box:
            answer_box_result["snippet"] += " ... " + answer_box["list"]
        if "source" in answer_box:
            answer_box_result["source"] = answer_box["source"]
        if "link" in answer_box:
            answer_box_result["link"] = answer_box["link"]
        full_results["answer_box"] = answer_box_result
        
    if "knowledge_graph" in results:
        # Set default values
        knowledge_graph_result = {}
        knowledge_graph_result["rank"] = "Knowledge Graph Result"
        knowledge_graph_result["title"] = ""  
        knowledge_graph_result["snippet"] = ""
        knowledge_graph_result["source"] = ""
        knowledge_graph_result["link"] = ""
        knowledge_graph_result["article_text"] = ""  # knowledge_graph results always have article_text empty
        
        knowledge_graph = results["knowledge_graph"]
        if "title" in knowledge_graph:
            knowledge_graph_result["title"] = knowledge_graph["title"]
            clean_title_list.append(knowledge_graph["title"])
        if "description" in knowledge_graph:
            knowledge_graph_result["snippet"] = knowledge_graph["description"]
        if "source" in knowledge_graph:
            if "name" in knowledge_graph["source"]:
                knowledge_graph_result["source"] = knowledge_graph["source"]["name"]
            if "link" in knowledge_graph["source"]:
                knowledge_graph_result["link"] = knowledge_graph["source"]["link"]
        full_results["knowledge_graph"] = knowledge_graph_result

    if "organic_results" in results:
        organic_results = []
        for i in range (min(len(results["organic_results"]), k)):  # return top k results from Google
            cur_result = results["organic_results"][i]
            
            organic_result = {}
            organic_result["rank"] = i + 1
            organic_result["title"] = cur_result["title"]
            organic_result["snippet"] = ""
            organic_result["source"] = cur_result["source"]
            organic_result["link"] = cur_result["link"]
            organic_result["article_text"] = ""
            clean_title_list.append(cur_result["title"])
            
            if "snippet" in cur_result:  # Some snippets can't be retrieved by SERPAPI
                organic_result["snippet"] = cur_result["snippet"]
            
            # parse article_text, discarded
            # if (cur_result["source"].strip().lower()) == "wikipedia":  
            #     organic_result["article_text"] = parse_wikipedia_article(cur_result["link"]) 
            # else: 
            #     temp_content = parse_other_article(cur_result["link"])
            #     if temp_content is not None:
            #         organic_result["article_text"] = temp_content
                
            organic_results.append(organic_result)
        full_results["organic_results"] = organic_results
        
    return clean_title_list, full_results


""" Debug """

if __name__ == "__main__":  # 记得科学上网
    serpapi_key = "42ba37659d4119f60b76efc5af3784bfea1363588cf89e10c11b9072d8e1354a"
    k = 3
    query = "How many games did Boston Celtics win in 2022?"
    # query = "Who is the 1993 World Champion figure skater?"
    # query = "British-Irish girl groups"
    
    clean_title_list, full_results = execute_web_query(query, serpapi_key, k)
    print("full_results:", full_results)
    
    # content = parse_wikipedia_article("https://en.wikipedia.org/wiki/1993_World_Figure_Skating_Championships")
    # print(content)
    
    # 403 Client Error
    # content = parse_other_article("https://www.volcanodiscovery.com/earthquakes/quake-info/9581069/mag1quake-Aug-31-2024-Sulawesi-Indonesia.html")
    
    # content = parse_other_article("https://www.britannica.com/science/atom")
    # content = parse_other_article("https://sankan.kunaicho.go.jp/english/guide/koukyo.html")
    # print(content)
    