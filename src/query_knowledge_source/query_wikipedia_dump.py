import requests

import re

# used for BGE and BM25
def extract_title_and_text(input_string):  
    # Define the regular expression to capture title and text
    pattern = r"Title:\s*(.*?)\s*Text:\s*(.*)"

    match = re.match(pattern, input_string)

    if match:
        # Extract title and text
        title = match.group(1)
        text = match.group(2)
        return title, text
    else:
        return "", text
    
    
# ColBERT
def retrieve_topk(query, n, url):
    params = {'query': query, 'k': n}
    response = requests.get(url=url, params=params)
    try:
        retrieved = response.json()["topk"]
    except Exception as e:
        print(f"+++ ColBERT Retrieval error at query \"{query}\"")
        print("Error:", e)
        return None
    
    return retrieved


# BGE
# def retrieve_topk(query, n, url):
#     response = requests.get(url, params={'query': query, 'k': n})
#     try:
#         # Parse the JSON response
#         response_json = response.json()
#         for entry in response_json:  
#             entry["prob"] = 0.7  # add dummy probability to align to ColBERT format
#             title, text = extract_title_and_text(entry["text"])
#             entry["text"] = (title.strip() + " | " + text.strip()).strip()
#         return response_json
#     except Exception as e:
#         print(f"+++ BGE Retrieval error at query \"{query}\"")
#         print("Error:", e)
#         return None


# BM25
# def retrieve_topk(query, n, url):
#     response = requests.get(url, params={'query': query, 'k': n})
#     try:
#         # Parse the JSON response
#         response_json = response.json()
#         extracted_results = []
#         cnt = 1
#         for entry in response_json["results"]:  
#             title, text = extract_title_and_text(entry["source"]["text"])
#             # add dummy probability to align to ColBERT format
#             extracted_entry = {"prob": 0.7, "rank": cnt, "text": (title.strip() + " | " + text.strip()).strip()}
#             extracted_results.append(extracted_entry)
#             cnt += 1
#         return extracted_results
#     except Exception as e:
#         print(f"+++ BM25 Retrieval error at query \"{query}\"")
#         print("Error:", e)
#         return None


if __name__ == "__main__":
    # print(retrieve_topk("William Shakespeare", 3, "http://localhost:9501/search"))  # BM25
    print(retrieve_topk("William Shakespeare", 3, "http://localhost:50002/retrieve"))  # BGE