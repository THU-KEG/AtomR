import os
os.environ["CUDA_VISIBLE_DEVICES"] = "4,5,6,7"

from colbert.infra import Run, RunConfig, ColBERTConfig
from colbert import Indexer

import time

if __name__=='__main__':
    
    s = time.time()
    
    # atlas dump
    with Run().context(RunConfig(nranks=1, experiment="atlas_full_wiki")):
        
        config = ColBERTConfig(
            nbits=2, 
            root="experiments"
        )
        indexer = Indexer(checkpoint="model_checkpoints/colbertv2.0", config=config)
        indexer.index(name="atlas_full_wiki.nbits=2", collection="/data/amy/WIKI_data/processed_tsv/atlas_202112_title_section+text_format_fixed.tsv")  # TODO: change to your own path

    print(f"\n*** Time: {str(time.time() - s)} ***")
    
