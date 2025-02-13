import os
os.environ["CUDA_VISIBLE_DEVICES"] = "0,1,2,3"

from colbert.infra import Run, RunConfig, ColBERTConfig
from colbert import Indexer

import time

if __name__=='__main__':
    
    s = time.time()
    
    # HotpotQA dump
    with Run().context(RunConfig(nranks=1, experiment="hotpotqa_wiki_abstracts")):
        
        config = ColBERTConfig(
            nbits=2, 
            root="experiments"
        )
        indexer = Indexer(checkpoint="model_checkpoints/colbertv2.0", config=config)
        indexer.index(name="hotpotqa_wiki_abstracts.nbits=2", collection="/data/amy/WIKI_data/processed_tsv/hotpotqa-20171001-abstracts.tsv")  # TODO: change to your own path

    print(f"\n*** Time: {str(time.time() - s)} ***")
    
