
# pdb学习

import requests
import time
from typing import Optional
import traceback

import sys
from query_knowledge_source.query_wikipedia_dump import retrieve_topk
from query_knowledge_source.query_google import execute_web_query
from query_knowledge_source.query_wikidata import kopl_semantic_parsing_api, kopl_engine_exec_api

import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# import nltk
# nltk.download('punkt') # need to download punkt tokenizer beforehand; function not compatible with vpn

import re
import ast


""" Global util functions """

def overlap_coefficient(set1: set, set2: set):
    intersection_size = len(set1.intersection(set2))
    smaller_set_size = min(len(set1), len(set2))
    if smaller_set_size == 0:
        return 0
    return intersection_size / smaller_set_size
    
    
""" Reasoning with a Local Text Corpus """

class Text:
    def __init__(self, retriever_api_url: Optional[str] = None, k: int = 3):
        if retriever_api_url is None:
            raise Exception("Text() instance initialization failed: no retriever_api_url provided.")
        self.retriever_api_url = retriever_api_url
        self.k = k
        
        print(f"Text instance initialized. retriever_api_url = '{self.retriever_api_url}', k = {self.k}")
    
    
    def retrieve_topk_passages(self, query: str, k: int, prob_threshold: float=1.0):
        retrieved = retrieve_topk(query, k, self.retriever_api_url)
        retry = 0
        while retrieved is None: 
            retry += 1
            print(f"Retry {retry}.")
            if (retry > 5):
                print("More than 5 retries, exiting.")
                exit()  
                # return None, None
            retrieved = retrieve_topk(query, k, self.retriever_api_url)
            time.sleep(5)
        
        # Format passages
        clean_entity_list = []
        entity_and_passage_list = []
        for entry in retrieved:
            split_index = entry["text"].find('|')  # ColBERT formatted passages into "title | section: text"
            entity = entry["text"][:split_index].strip()
            passage = entry["text"][split_index + 1:].strip()
            prob = entry["prob"]
            rank = entry["rank"]
            
            clean_entity_list.append(entity)
            entity_and_passage_list.append({"entity": entity, "passage": passage, "rank": rank, "prob": prob})
            
            if prob > prob_threshold:  # only take top1 passage if its probability surpasses given threshold
                break
                    
        return clean_entity_list, entity_and_passage_list
    
    
    def Search(self, question: str, entity_name: str, descriptors: Optional[str] = ""):
        query = f"{entity_name.strip()} {descriptors.strip()}"
        clean_entity_list, entity_and_passage_list = self.retrieve_topk_passages(query, self.k, prob_threshold=0.75)
        
        return clean_entity_list, entity_and_passage_list


    def Relate(self, question: str, entity: str, relation: str):
        query = f"{entity.strip()} {relation.strip()}"
        clean_entity_list, entity_and_passage_list = self.retrieve_topk_passages(query, self.k, prob_threshold=0.85)  # higher prob threshold than search because relations are more ambiguous
        
        return clean_entity_list, entity_and_passage_list
    
        
    def Filter(self, question: str, entities: list, condition: str):
        filtered_entity_score_dict = {}
        filtered_entity_passage_dict = {}
        for entity in entities:
            query = f"{entity} {condition}"
            top1_clean, top1_full = self.retrieve_topk_passages(query, 1)  # only retrieve top1 passage for each entity in Filter()
            if top1_full is None:  # skip entity if cannot retrieve passage
                continue
            top1_full = top1_full[0]  # get top1 passage's dict
            passage_with_title = f"{top1_full['entity']} {top1_full['passage']}"
            passage_with_title_wordset = set(passage_with_title.lower().split())
            
            # Use overlap coefficient to filter entity passages
            entity_and_condition_wordset = set(query.lower().split())
            overlap_coeff = overlap_coefficient(entity_and_condition_wordset, passage_with_title_wordset)
            if overlap_coeff >= 0.5:
                entity = top1_full["entity"]
                filtered_entity_score_dict[entity] = overlap_coeff
                filtered_entity_passage_dict[entity] = top1_full["passage"]
        
        if len(filtered_entity_score_dict) == 0:
            return None, None
        
        print("filtered_entity_score_dict:", filtered_entity_score_dict)  # debug
        
        # Sort entities by overlap coeff in descending order
        final_entity_and_score_list = sorted(filtered_entity_score_dict.items(), key=lambda item: item[1], reverse=True)
        if final_entity_and_score_list[0][1] >= 0.85: # If exists passage entities with very high overlap score, discard the ones with lower score
            discard_index = 0
            for entity in final_entity_and_score_list:
                if entity[1] < 0.85:
                    final_entity_and_score_list = final_entity_and_score_list[:discard_index]
                    break
                discard_index += 1 
                
        final_clean_entity_list = []
        final_entity_and_passage_list = []  # format final filtered passages list to feed to LLM
        rank = 1
        for entry in final_entity_and_score_list:
            entity = entry[0]
            final_clean_entity_list.append(entity)
            final_entity_and_passage_list.append({"entity": entity, "passage": filtered_entity_passage_dict[entity], "overlap_coeff": filtered_entity_score_dict[entity], "rank": rank}) 
            rank += 1
        
        return final_clean_entity_list, final_entity_and_passage_list
                 
    
""" Reasoning with a Web Search Engine """

class Web: 
    def __init__(self, serpapi_key: str = None, k: int = 3):
        if serpapi_key is None:
            raise Exception("Web() instance initialization failed: no serpapi_key provided.")
        self.serpapi_key = serpapi_key
        self.k = k
        
        print(f"Web instance initialized. serpapi_key = '{self.serpapi_key}', k = {self.k}.")
    
    
    def retrieve_topk_articles(self, query: str, k: int):
        try:
            clean_title_list, full_results = execute_web_query(query, self.serpapi_key, k)
        except Exception as e:
            retry = 1
            print(f"Google results retrieval error at query \'{query}\'")
            print("Exception:", e)
            full_results = None
            while full_results is None:
                if retry > 3:
                    return None, None  # retrieval error for current query
                time.sleep(5)
                try:
                    print(f"Retry {retry}")
                    clean_title_list, full_results = execute_web_query(query, self.serpapi_key, k)
                except:
                    print("Exception:", e)
                    retry += 1
                
        return clean_title_list, full_results
    
    
    def break_article_into_passages(self, text: str, max_length: int = 250, overlap: int = 100):  # break article text into passages of `max_length` characters with `overlap` number of characters
        passages = []
        start = 0
        while start < len(text):
            if start + max_length > len(text):
                passages.append(text[start:])
                break
            end = start + max_length
            while end < len(text) and text[end] not in " \n": # ensure we don't cut words in half
                end += 1
            passages.append(text[start:end])
            start += max_length - overlap
        return passages
    
    
    def Search(self, question: str, entity_name: str, descriptors: Optional[str] = ""):
        query = f"{entity_name.strip()} {descriptors.strip()}"
        
        # Retrieve Google articles
        clean_title_list, full_results = self.retrieve_topk_articles(query, self.k)
        if "answer_box" not in full_results and "knowledge_graph" not in full_results and "organic_results" not in full_results:
            return None, None
        
        return clean_title_list, full_results
    
    
    def Relate(self, question: str, entity: str, relation: str):
        query = f"{entity.strip()} {relation.strip()}"
        # query = question  # question search more likely to get answer box, but less accurate
        
        # Retrieve Google articles
        clean_title_list, full_results = self.retrieve_topk_articles(query, self.k)
        if "answer_box" not in full_results and "knowledge_graph" not in full_results and "organic_results" not in full_results:
            return None, None
        
        return clean_title_list, full_results
        
        
    def Filter(self, question: str, entities: list, condition: str):
        filtered_entity_score_dict = {}
        filtered_entity_passages_dict = {}
        filtered_entity_results_dict = {}
        for entity in entities:
            query = f"{entity} {condition}"
            top1_clean_title_list, top1_full_results = self.retrieve_topk_articles(query, 1)
            print(query)
            if "answer_box" not in top1_full_results and "knowledge_graph" not in top1_full_results and "organic_results" not in top1_full_results:
                continue   # skip entity if cannot retrieve article
            
            print("top1_full_results non-empty")
            filtered_entity_results_dict[entity] = top1_full_results
            entity_condition_wordset = set(query.lower().split())
            
            # Concatenate snippets and passages from each answer type
            snippets_and_passages = []
            if "answer_box" in top1_full_results:
                snippets_and_passages.append(f"{top1_full_results['answer_box']['title']} | {top1_full_results['answer_box']['snippet']}")  # adding "|" only to ease human view
            if "knowledge_graph" in top1_full_results:
                snippets_and_passages.append(f"{top1_full_results['knowledge_graph']['snippet']} | {top1_full_results['knowledge_graph']['snippet']}")
            if "organic_results" in top1_full_results:
                organic_result_top1 = top1_full_results["organic_results"][0]
                organic_result_str = f"{organic_result_top1['title']} | {organic_result_top1['snippet']}"
                snippets_and_passages.append(organic_result_str)
            
            snippets_and_passages_string = " ... ".join(snippets_and_passages)
            snippets_and_passages_wordset = set(snippets_and_passages_string.lower().split())
            
            # Use overlap coefficient to filter entity passages
            overlap_coeff = overlap_coefficient(entity_condition_wordset, snippets_and_passages_wordset)
            print("overlap_coeff:", overlap_coeff)
            if overlap_coeff >= 0.5:
                filtered_entity_score_dict[entity] = overlap_coeff
                filtered_entity_passages_dict[entity] = snippets_and_passages_string
                print("overlap_coeff >= 0.5")
        
        if len(filtered_entity_score_dict) == 0:
            return None, None
        
        print("filtered_entity_score_dict:", filtered_entity_score_dict)  # debug
        
        # Sort entities by overlap coeff in descending order
        final_entity_and_score_list = sorted(filtered_entity_score_dict.items(), key=lambda item: item[1], reverse=True)
        if final_entity_and_score_list[0][1] >= 0.85: # If exists passage entities with very high overlap score, discard the ones that are lower-scored
            discard_index = 0
            for entity in final_entity_and_score_list:
                if entity[1] < 0.85:
                    final_entity_and_score_list = final_entity_and_score_list[:discard_index]
                    break
                discard_index += 1 
        
        final_entity_list = []
        final_entity_results_dict = {}  # format final filtered passages list to feed to LLM
        rank = 1
        for entry in final_entity_and_score_list:
            entity = entry[0]
            final_entity_list.append(entity)
            final_entity_results_dict[entity] = filtered_entity_results_dict[entity]
            rank += 1
        
        return final_entity_list, final_entity_results_dict


""" Reasoning with Wikidata """

class KB: 
    def __init__(self, kb_query_language: Optional[str] = None, kopl_parser_url: Optional[str] = None, kopl_engine_url: Optional[str] = None):
        if kb_query_language.lower().strip() != "kopl":
            raise Exception("kb_query_language error: our current system only supports the KoPL language for KB queries. Exiting.")
        self.kb_query_language = kb_query_language.strip()
        
        if kopl_parser_url is not None:
            self.kopl_parser_url = kopl_parser_url
        else:
            self.kopl_parser_url = "https://viskop.xlore.cn/programApi"  # KoPL's official semantic parser API
        
        if kopl_engine_url is not None:
            self.kopl_engine_url = kopl_engine_url
        else:
            self.kopl_engine_url = "https://viskop.xlore.cn/large"  # KoPL's official KB engine API
            
        print(f"KB instance initialized. kb_query_language = '{self.kb_query_language}', kopl_parser_url = '{self.kopl_parser_url}', kopl_engine_url = '{self.kopl_engine_url}'")
            
    
    def obtain_kopl_results(self, question: str):
        try:
            program = kopl_semantic_parsing_api(question, self.kopl_parser_url)
        except Exception as e:
            retry = 1
            print(f"+++ KoPL semantic parsing error occured at query \'{question}\'")
            print("Exception:", e)
            program = None
            while program is None:
                if retry >= 3:
                    return None, None  # KoPL error for current query
                time.sleep(5)
                try:
                    print(f"Retry {retry}")
                    program = kopl_semantic_parsing_api(question, self.kopl_parser_url)
                except:
                    print("Exception:", e)
                    retry += 1
        
        try:
            json_answers = kopl_engine_exec_api(program, self.kopl_engine_url)
        except Exception as e:     
            retry = 1
            print(f"+++ KoPL engine execution error occured at query \'{question}\'")
            print("Exception:", e)
            json_answers = None
            while json_answers is None:
                if retry >= 3:
                    return None, None  # KoPL error for current query
                time.sleep(5)
                try:
                    print(f"Retry {retry}")
                    json_answers = kopl_engine_exec_api(program, self.kopl_engine_url)
                except:
                    print("Exception:", e)
                    retry += 1
        
        clean_answer_list = []
        try:
            clean_answer_list = json_answers["inner_content"][-1]["content"]  
        except Exception as e:
            print(f"!!! Error parsing [\"content\"] from KoPL json_answers. Returning [\"answer\"]: {json_answers['answer']}")
            if json_answers["answer"] == "Not Found in KB":
                return None, None
            clean_answer_list = [json_answers["answer"]]
            
        if len(clean_answer_list) == 0:
            return None, None
        
        if len(clean_answer_list) > 10:   # keep first 10 answers
            clean_answer_list = clean_answer_list[:10]
    
        return clean_answer_list, json_answers
    
    
    def Search(self, question: str, entity_name: str, descriptors: Optional[str] = ""):
        if descriptors != "":
            query = f"{question} ({descriptors})"
        else:
            query = question
            
        clean_answer_list, json_answers = self.obtain_kopl_results(query)  
        if clean_answer_list is None:
            if descriptors == "":
                clean_answer_list = [entity_name]
            else:
                clean_answer_list = [f"{entity_name} ({descriptors})"]
        
        return clean_answer_list, json_answers
    
    
    def Relate(self, question: str, entity: str, relation: str):
        clean_answer_list, json_answers = self.obtain_kopl_results(question)
        return clean_answer_list, json_answers
        
        
    def Filter(self, question: str, entities: list, condition: str):
        clean_answer_list, json_answers = self.obtain_kopl_results(question)          
        return clean_answer_list, json_answers
    
