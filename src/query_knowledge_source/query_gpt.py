import requests
import json
import time
from typing import Optional
import os

""" Querying GPT-4o via OpenAI service """

class OpenAICaller():
    def __init__(self, api_url: Optional[str]="http://127.0.0.1:9998/api/openai/chat_completion", 
                 cache_path: Optional[str]="TOCHANGE"):
        self.api_url = api_url            
            
        self.cache = {}
        print(cache_path)
        self.cache_path = cache_path
        os.makedirs(os.path.dirname(self.cache_path), exist_ok=True)  # create cache path if it doesn't exist
        
        if os.path.exists(self.cache_path):
            with open(self.cache_path, "r") as f:
                for line in f:
                    entry = json.loads(line.strip())
                    self.cache[tuple(entry["input"])] = entry["response"]
                f.close()
                
    
    def query_gpt4o(self, prompt, model="gpt-4o-2024-08-06", temperature=0, max_tokens=128, use_cache=True):  # use_cache should be True, changed for debug purposes only
            input = (prompt, model, max_tokens)
            if use_cache and temperature == 0 and input in self.cache:  # if input requested before, directly return from cache
                print("use_cache.")  # debug
                cache_response = self.cache[input]
                response_text = cache_response[0]['message']['content']
                finish_reason = cache_response[0]['finish_reason']
                return response_text, finish_reason
            
            try:
                response = requests.post(self.api_url, json = {
                        "model": model,
                        "prompt": prompt,
                        "temperature": temperature,
                        "max_tokens": max_tokens,
                })
                if response.status_code != 200:
                    raise Exception("[OpenAI Response Error]:", response.text)
            except Exception as e:
                raise Exception("[OpenAI Call Error]:", e)
            
            # Extract LLM response
            try:
                response = response.json()['choices']
                # print("[OpenAI Response]:", response)  # debug
                finish_reason = response[0]['finish_reason']
                response_text = response[0]['message']['content']
            except:
                raise Exception("[OpenAI Call Error]:", e)
            
            # Store response to cache
            if temperature == 0:
                input = (prompt, model, max_tokens)
                res = response[0]
                if input not in self.cache:
                    self.cache[input] = [res]
                    with open(self.cache_path, "a") as f:
                        f.write("%s\n"%json.dumps({"input": input, "response": [res]}))
                        f.close()
            
            return response_text, finish_reason


if __name__ == "__main__":
    # Test GPT4o
    openai_caller = OpenAICaller(cache_path="TOCHANGE")
    response, finish_reason = openai_caller.query_gpt4o(prompt="Morning!", max_tokens=8, use_cache=True)
    print("response:", response)
    print("finish_reason:", finish_reason)
    