# from colbert.data import Queries
# from colbert.infra import Run, RunConfig, ColBERTConfig
# from colbert import Searcher
# import math

# if __name__=='__main__':
#     # hotpotqa
#     # with Run().context(RunConfig(nranks=1, experiment="hotpotqa_wiki_abstracts_searchain")):
    
#     # DPR dump
#     with Run().context(RunConfig(nranks=1, experiment="dpr_first100")):

#         config = ColBERTConfig(
#             root="/ColBERT-main/experiments",
#         )
#         # hotpotqa
#         # searcher = Searcher(index=f"hotpotqa_wiki.nbits=2")
        
#         # DPR
#         searcher = Searcher(index=f"dpr_first100_wiki.nbits=2")
#         # queries = Queries("/path/to/MSMARCO/queries.dev.small.tsv")
#         # ranking = searcher.search_all(queries, k=100)
        
#         # query = "What number airline is Hana Hou!"  # r1 = Hana Hou! 
#         # query = "British-Irish girl group based in London"  # r1 = The Saturdays (p=0.76), r2 = British and Irish Communist Organization (0.18), r3 = One Direction (0.05)
#         # query = "British-Irish girl group filled 2 positions in the voice of ireland"  # r1 = The Voice (p=0.35), r2 = Una Healy (member of The Saturdays, p=0.33), r3 = The Voice of Ireland (mentions "The Saturdays", p=0.32)
#         # query = "Which maker of Robatumumab is American?"  # r1 = Robatumumab (p=0.96), r2 = (p=0.020), r3 = (p=0.015)
#         # query = "Robatumumab"
#         # query = "Robatumumab maker"  # r1 = Robatumumab (p=0.99)
#         # query = "Robatumumab maker American"  # r1 = Robatumumab (p=0.92, 比问句低interesting)
        
#         query = "Aaron"
        
#         pids, ranks, scores = searcher.search(query, k=100)
#         pids, ranks, scores = pids[:3], ranks[:3], scores[:3]
        
#         probs = [math.exp(score) for score in scores]
#         probs = [prob / sum(probs) for prob in probs]
        
#         topk = []
#         for pid, rank, score, prob in zip(pids, ranks, scores, probs):
#             text = searcher.collection[pid]            
#             d = {'text': text, 'pid': pid, 'rank': rank, 'score': score, 'prob': prob}
#             topk.append(d)
#         topk = list(sorted(topk, key=lambda p: (-1 * p['score'], p['pid'])))
        
#         print(topk)
        
#         # ranking.save("msmarco.nbits=2.ranking.tsv")
        
        
# Created by Amy

# from colbert.data import Queries
# from colbert.infra import Run, RunConfig, ColBERTConfig
# from colbert import Searcher
import math
import requests


def test_api_retrieval_hotpotqa(query, n=3):
    url = 'http://localhost:1212/api/search'
    params = {'query': query, 'k': n}
    response = requests.get(url, params=params)

    print("Query:", query)
    print(response.json()["topk"])
    print()
    
    
def test_api_retrieval_dpr(query, n=3):
    url = 'http://localhost:1213/api/search'
    params = {'query': query, 'k': n}
    response = requests.get(url, params=params)

    print("Query:", query)
    print(response.json()["topk"])
    print()


def test_api_retrieval_atlas(query, n=3):
    url = 'http://localhost:1214/api/search'
    params = {'query': query, 'k': n}
    response = requests.get(url, params=params)

    print("Query:", query)
    print(response.json()["topk"])
    print()


# def test_local_retrieval_hotpotqa(query, n):  # TODO: debug
#     with Run().context(RunConfig(nranks=1, experiment="/data1/amy/00Engine/ColBERT/experiments/hotpotqa_wiki_abstracts")):

#         # config = ColBERTConfig(
#         #     root="",
#         # )
#         searcher = Searcher(index=f"hotpotqa_wiki.nbits=2")  # config=config useless
#         # queries = Queries("/path/to/MSMARCO/queries.dev.small.tsv")
#         # ranking = searcher.search_all(queries, k=100)
        
#         pids, ranks, scores = searcher.search(query, k=100)
#         pids, ranks, scores = pids[:n], ranks[:n], scores[:n]
        
#         probs = [math.exp(score) for score in scores]
#         probs = [prob / sum(probs) for prob in probs]
        
#         topk = []
#         for pid, rank, score, prob in zip(pids, ranks, scores, probs):
#             text = searcher.collection[pid]            
#             d = {'text': text, 'pid': pid, 'rank': rank, 'score': score, 'prob': prob}
#             topk.append(d)
#         topk = list(sorted(topk, key=lambda p: (-1 * p['score'], p['pid'])))
        
#         print(topk)
        
#         # ranking.save("msmarco.nbits=2.ranking.tsv")
        
        
# def test_local_retrieval_dpr(query, n):
#     with Run().context(RunConfig(nranks=1, experiment="dpr_first100")):

#         config = ColBERTConfig(
#             root="experiments",
#         )
#         searcher = Searcher(index=f"dpr_first100_wiki.nbits=2", config=config)  # config=config added
#         # queries = Queries("/path/to/MSMARCO/queries.dev.small.tsv")
#         # ranking = searcher.search_all(queries, k=100)
        
#         pids, ranks, scores = searcher.search(query, k=100)
#         pids, ranks, scores = pids[:n], ranks[:n], scores[:n]
        
#         probs = [math.exp(score) for score in scores]
#         probs = [prob / sum(probs) for prob in probs]
        
#         topk = []
#         for pid, rank, score, prob in zip(pids, ranks, scores, probs):
#             text = searcher.collection[pid]            
#             d = {'text': text, 'pid': pid, 'rank': rank, 'score': score, 'prob': prob}
#             topk.append(d)
#         topk = list(sorted(topk, key=lambda p: (-1 * p['score'], p['pid'])))
        
#         print(topk)
        

if __name__=='__main__':
    
    #### Searchain format wiki dumps (Title: / Text: ...)
    
    # gt - ground truth, hgt - half ground truth (contain related info)
    # query = "What number airline is Hana Hou!"  # r1 = Hana Hou! 
    # query = "British-Irish girl group based in London"  # r1 = [gt]The Saturdays (p=0.76), r2 = British and Irish Communist Organization (0.18), r3 = One Direction (0.05)
    # query = "British-Irish girl group filled 2 positions in the voice of ireland"  # r1 = The Voice (p=0.35), r2 = [gt]Una Healy (member of The Saturdays, p=0.33), r3 = [hgt]The Voice of Ireland (mentions "The Saturdays", p=0.32)
    # query = "Which maker of Robatumumab is American?"  # r1 = [gt]Robatumumab (p=0.96), r2 = (p=0.020), r3 = (p=0.015)
    # query = "Robatumumab"
    # query = "Robatumumab maker"  # r1 = [gt]Robatumumab (p=0.99)
    # query = "Robatumumab maker American"  # r1 = [gt]Robatumumab (p=0.92, 比问句低interesting)
    # query = "Merck and Schering Plough, American"  # r1 = [hgt]Schering-Plough (p=0.78), r2 = Organon (p=0.17), r3 = Coppertone (p=0.05)
    
    # test_api_retrieval(query="Merck, American", n=3)  # [gt]Merck & Co (0.58), [hgt]Merck family (0.26), Merck Mercuriadis 
    # test_api_retrieval(query="Is Merck American?", n=3) # [gt]Merck & Co (0.59), [hgt]Merck family (0.26), [hgt]The Merck Manuals (0.135)
    # test_api_retrieval(query="Schering Plough, American", n=3)  # [gt]Schering Plough (0.698), [hgt]Richard Kogan (0.22), Ernst Christian Friedrich Schering (0.08)
    # test_api_retrieval(query="Is Schering Plough American?", n=3)  # [gt]Schering Plough (0.688), [hgt]Richard Kogan (0.26), [hgt]Organon (0.05)
    # test_api_retrieval_hotpotqa(query="Which of Merck and Schering Plough is American?", n=3)  # [hgt]Schering Plough(0.75), [hgt]Organon International(0.133), [hgt]Coppertone(0.115) # 不适合直接做多跳/多约束问题查询
    
    # test_api_retrieval_hotpotqa(query="Arithmetic", n=3)  # searchain format, Arithmetic (0.62)
    # test_api_retrieval_hotpotqa(query="What is Arithmetic?", n=3)  # Arithmetic (0.50)
    # test_api_retrieval_hotpotqa(query="Title: Arithmetic", n=3)  # Arithmetic (0.46)
    
    # test_local_retrieval_dpr(query="Aaron", n=3)  # Aaron (0.793), 0.104, 0.103
    # test_local_retrieval_dpr(query="Aaron | ", n=3)  # Aaron (0.798), 0.110, 0.092, 区别不大
    
    
    #### DPR Format wiki dumps (Title | Text )
    
    # test_api_retrieval_hotpotqa(query="Arithmetic", n=3)  # our format, Arithmetic (0.56)
    
    # test_api_retrieval_hotpotqa(query="Britain's House of Hanover", n=3)  # 0.905
    # test_api_retrieval_hotpotqa(query=" What is Britain's House of Hanover?", n=3)  # 0.903
    
    # test_api_retrieval_hotpotqa(query="George IV date of death", n=3)  # 0.718
    # test_api_retrieval_hotpotqa(query="When did George IV die?", n=3)  # 0.691
    
    # test_api_retrieval_hotpotqa(query="Erika Cheung", n=3)  # 0.691
    
    # FEVER question 30
    # test_api_retrieval_hotpotqa(query="Mel B release song 2007", n=3)  
    # test_api_retrieval_hotpotqa(query="Mel B released a song on Virgin Records in 2007", n=5)  
    
    # Hotpotqa question 501
    # test_api_retrieval_hotpotqa(query="Kim Dae-woo", n=3)  # 0.59
    # test_api_retrieval_hotpotqa(query="Kim Dae-woo film director", n=3)  # 0.89
    # test_api_retrieval_hotpotqa(query="Kim Dae-woo (film director)", n=3)  # 0.86
    # test_api_retrieval_hotpotqa(query="Kim Dae-woo directing debut film", n=3)  # 0.94
    # test_api_retrieval_hotpotqa(query="What was Kim Dae-woo's directing debut film?", n=3)  # 0.89
    # test_api_retrieval_hotpotqa(query="Forbidden Quest person about", n=3)  # 0.90
    
    # Hotpotqa question 502
    # test_api_retrieval_hotpotqa(query="Who is the man known for a science humor story based on the tongue-in-cheek combination of two adages?", n=3)  
    # test_api_retrieval_hotpotqa(query="Who is the man known for Buttered cat paradox?", n=3)  # 0.94
    # test_api_retrieval_hotpotqa(query="Buttered cat paradox man known for", n=3)  # 0.86

    # Hotpotqa question 503
    # test_api_retrieval_hotpotqa(query="What was the plane type used for BOAC Flight 911?", n=3)  # 0.99
    # test_api_retrieval_hotpotqa(query="BOAC Flight 911", n=3)  # 1.00
    # test_api_retrieval_hotpotqa(query="BOAC Flight 911 plane type", n=3)  # 0.99
    # test_api_retrieval_hotpotqa(query="Beoing 707-436 largest passenger capacity", n=3)  # 0.69
    
    # Hotpotqa question 504
    # test_api_retrieval_hotpotqa(query="Anglo-Irish actress, courtesan, and mistress who was the mother to the illegitimate daughter of King William IV", n=3)  # not enough info
    # test_api_retrieval_hotpotqa(query="mother to the illegitimate daughter of King William IV", n=3)  # not enough info
    
    # test_api_retrieval_hotpotqa(query="King William IV", n=3)  # 0.80
    # test_api_retrieval_hotpotqa(query="illegitimate daughter of King William IV", n=5)  # 3 daughters, 0.48, 0.22, 0.20
    # test_api_retrieval_hotpotqa(query="Lady Mary Fox mother to", n=3)  # 0.93，但不确定能不能正确抽出“mistress Dorothea Jordan"
    
    # test_api_retrieval_hotpotqa(query="Anglo-Irish actress, courtesan, and mistress", n=3)  # 0.93
    # test_api_retrieval_hotpotqa(query="Dorothea Jordan Anglo-Irish actress, courtesan, and mistress", n=3)  # 1.00
    
    # test_api_retrieval_hotpotqa(query="Dorothea Jordan birthday", n=3)  # 1.00
    
    # Musique
    
    # test_api_retrieval_atlas(query="Which war did the Finnish Navy serve in?", n=3)  # gt "Winter War" not retrieved in top 3
    # test_api_retrieval_atlas(query="Finnish Navy served in war", n=3)   # gt "Winter War" retrieved at 1
    # test_api_retrieval_atlas(query="Finnish Navy served in", n=3)   # gt "Winter War" not retrieved in top 3

    # test_api_retrieval_atlas("Who is the wrestler who has held the intercontinental championship the most times?")  # top1 passage里居然包含了答案, 0.423
    # test_api_retrieval_atlas("wrestler held the intercontinental championship the most times")  # rank2, 可能因为缺少了who has held关键词
    # test_api_retrieval_atlas("wrestler who has held the intercontinental championship the most times")  # rank1, 0.420
    # test_api_retrieval_atlas("Where did Chris Jericho win in 2008?")
    # test_api_retrieval_atlas("Chris Jericho won at competition in 2008")
    
    # test_api_retrieval_atlas("Who is the father of James Mayer de Rothschild?")  # 0.55
    # test_api_retrieval_atlas("father of James Mayer de Rothschild")  # 0.50
    # test_api_retrieval_atlas("James Mayer de Rothschild father")  # 0.54
    
    # test_api_retrieval_atlas("First black student admitted to Mississippi Delta Community College")
    # test_api_retrieval_atlas("Mississippi Delta Community College first black student admitted")
    
    # test_api_retrieval_atlas("KABG")
    # test_api_retrieval_atlas("KABG is located at city")
    # test_api_retrieval_atlas("In which county is Albuquerque located in")  # 0.48
    # test_api_retrieval_atlas("Albuquerque is located in county")  # 0.57
    # test_api_retrieval_atlas("Albuquerque located in county")  # 0.54
    
    # test_api_retrieval_hotpotqa("Coke Kahani 2012 Pakistani comedy drama sitcom")  # 1.00, Coke Kahani
    # test_api_retrieval_hotpotqa("Coke Kahani writers")  # 1.00, Syed Mohammad Ahmed, Yasir Rana (but only mentioned Yasir Hussain as actor)
    # test_api_retrieval_hotpotqa("Coke Kahani writer who helped write for") # 0.98, still same passage that mentions Yasir Hussain as actor
    # test_api_retrieval_hotpotqa("Pakistani actor and writer from Islamabad")  # 0.73, Yasir Hussain
    
    # test_api_retrieval_hotpotqa("F. Javier gutierrez film director")  # 0.98, F. Javier Gutiérrez
    # test_api_retrieval_hotpotqa("F. Javier gutierrez directed movie")  # 0.91, Brazil, Norman's Room, film debut Before the Fall; 0.073, Rings (2017 film), directed by F. Javier Gutiérrez
    # test_api_retrieval_hotpotqa("Brazil starring actress")
    # test_api_retrieval_hotpotqa("Norman's Room starring actress")
    # test_api_retrieval_hotpotqa("Before the Fall starring actress")
    # test_api_retrieval_hotpotqa("Rings (2017 Film) starring actress")  # 0.92, Matilda Lutz; 0.04, Matilda Lutz
    # test_api_retrieval_hotpotqa("Italian model and actress", n=5)
    
    # test_api_retrieval_hotpotqa("ten-school collegiate athletic conference headquartered in Irving, Texas")  # gt top 1, 0.51
    # test_api_retrieval_hotpotqa("What baseball teams are part of the Big 12 Conference?")  # gt top 2, 0.38
    # test_api_retrieval_hotpotqa("Big 12 Conference baseball team")  # gt top 1, 0.46
    # test_api_retrieval_hotpotqa("baseball team coached by Randy Mazey in 2016")
    
    # test_api_retrieval_hotpotqa("What science fantasy young adult series is told in first person?")
    test_api_retrieval_atlas("What science fantasy young adult series is told in first person?")
    