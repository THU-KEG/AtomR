import requests
from requests.exceptions import RequestException
import datetime

def kopl_engine_exec_api(program, api_url):
    # url = "https://viskop.xlore.cn/large"
    # url = "http://localhost:55010/large"  # zhicheng
    # url = "http://localhost:65010/large" # mine from 19
    url = api_url

    payload = {'program': program}
    files=[]
    headers = {}

    response = requests.request("POST", url, headers=headers, 
                                json=payload, files=files, timeout=60)
    
    print("kopl_engine_exec_api:", response)
    
    if response.status_code != 200:
        return {"answer": "Not Found in KB"}
    
    return response.json()

def kopl_semantic_parsing_api(question, api_url):
    # url = "https://viskop.xlore.cn/programApi"
    # url = "http://localhost:5101/programApi"  # zhicheng
    # url = "http://127.0.0.1:6101/programApi"  # mine in 34, 巨慢
    # url = "http://localhost:8505/programApi"  # mine in 37
    url = api_url

    payload = {'question': question}
    files=[]
    headers = {}

    response = requests.request("POST", url, headers=headers, data=payload, files=files)
    
    print("kopl_semantic_parsing_api:", response)
    # exit()

    return response.json()['program']


""" Debug """

def main():
    start = datetime.datetime.now()

    # question = "When did China join WTO?"
    # question = "Which country shares border with Germany and France?"
    question = "Who is taller, LeBron James or Kobe Byrant?"
    # question = "What countries share a border with both Germany and France?"
    # question = "What is the capital of France?"
    # question = "How many Critics' Choice Movie Awards were nominations for the film whose official website is http://www.moonrisekingdom.com?"
    # question = "Where is Tsinghua University"
    # question = "Was Rod Serling the person who wrote over half of the episodes of Twilight Zone?"
    # question = "Who is the prime minister of United Kingdom?"

    # question = "When did Canada win its second Winter Games gold medal?"
    # question = "Who of these screenwriters co-wrote a film starring Nicolas Cage and Téa Leoni?"
    # question = "What is the charater role of Colm Meaney in Star Trek: Deep Space Nine?"
    # question = "Who is the mother of Mary Robinson in Shakespeare's \"The Winter Tale\""
    
    print("before semantic parsing")
    program = kopl_semantic_parsing_api(question, api_url="http://localhost:8505/programApi")
    print(question)
    print(program)

    print("before kopl engine")
    response = kopl_engine_exec_api(program, api_url="http://localhost:65010/large")
    print(response)
    print(response['answer'])
    # print(response['inner_content'][-1])

    end = datetime.datetime.now()
    print("time_taken: ", end-start)
    
if __name__ == '__main__':
    main()