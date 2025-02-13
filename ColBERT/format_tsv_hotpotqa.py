"""
    Convert raw hotpotqa wiki abstract dump into tsv file for ColBERT indexing.
    3 namefields: id, text, title
    Format: "{Title} | {Passage}"
"""

import json
import bz2
import os
import csv

def main():
    # TODO: change to your own paths
    data_path = '/data1/amy/WIKI_data/raw_originals/hotpotqa-enwiki-20171001-pages-meta-current-withlinks-abstracts'
    output_path = '/data1/amy/WIKI_data/processed_tsv/hotpotqa_20171001_abstracts.tsv'
    
    with open(output_path, 'w', encoding='utf-8-sig') as w:

        fieldnames = ['id', 'text', 'title']
        writer = csv.DictWriter(w, fieldnames=fieldnames, delimiter='\t')
        
        # Write headers
        writer.writeheader()
        
        # Walk through directory
        _id = 1
        for root, dirs, files in os.walk(data_path):
            for file in files:
                file_path = os.path.join(root, file)
                with bz2.open(file_path, 'rt', encoding='utf-8') as fin:
                    for line in fin:
                        data = json.loads(line)
                        row_text = ' '.join(data['text'])
                        # Write each row as a dictionary
                        writer.writerow({'id': _id, 'title': data['title'], 'text': row_text})
                        _id += 1
                        
                        if (_id % 1000 == 0):
                            print(_id)
        
    print(f"Formatting completed. TSV file saved to '{output_path}'.")


if __name__=='__main__':
    main()
    