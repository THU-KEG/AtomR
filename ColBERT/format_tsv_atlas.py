"""
    Convert raw atlas full wiki dump into tsv file for ColBERT indexing.
    3 namefields: id, text, title
    Passage: "{Title} | {Section}: {Text}"
"""

import json

def main():
    # TODO: change to your own paths
    data_path = '/data1/amy/WIKI_data/raw_originals/atlas_enwiki_202112/atlas_eniki_202112/corpora/wiki/enwiki-dec2021/text-list-100-sec.jsonl'
    output_path = '/data1/amy/WIKI_data/processed_tsv/atlas_202112_title_section+text.tsv'
        
    with open(data_path, 'r') as jsonl_file, open(output_path, 'w') as tsv_file:
        tsv_file.write("id\ttext\ttitle\n")
        
        count = 0
        for line in jsonl_file:
            entry = json.loads(line)
            
            id = int(entry['id']) + 1  # colbert requires id to start from 1
            title = entry['title']
            
            if len(entry['section']) == 0:
                text = entry['text']
            else:
                text = f"{entry['section']}: {entry['text']}"
            
            # remove extra newlines to avoid tsv reading bugs
            text = text.replace('\n', '')
            title = title.replace('\n', '')
            tsv_line = f"{id}\t{text}\t{title}\n"
            
            tsv_file.write(tsv_line)
            
            count += 1
            
            if (count % 10000 == 0):
                print(count)

    print(f"Formatting completed. TSV file saved to '{output_path}'.")
    
    
if __name__=='__main__':
    main()
