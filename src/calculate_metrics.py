import json
import re
import string
from collections import Counter

# Evaluate final results for all methods


def normalize_answer(s):

    def remove_articles(text):
        return re.sub(r'\b(a|an|the)\b', ' ', text)

    def white_space_fix(text):
        return ' '.join(text.split())

    def remove_punc(text):
        exclude = set(string.punctuation)
        return ''.join(ch for ch in text if ch not in exclude)

    def replace_hyphens(text):
        return text.replace("-", " ")
    
    def lower(text):
        return text.lower()

    return white_space_fix(remove_articles(remove_punc(replace_hyphens(lower(s))))).strip()


def calculate_f1(prediction, gold_list):
    max_f1 = 0.0
    prediction = normalize_answer(prediction)
    
    for gold in gold_list:
        gold = normalize_answer(gold)
        
        prediction_tokens = prediction.split()
        ground_truth_tokens = gold.split()
        common = Counter(prediction_tokens) & Counter(ground_truth_tokens)
        num_same = sum(common.values())
        if num_same == 0:
            continue
        
        precision = 1.0 * num_same / len(prediction_tokens)
        recall = 1.0 * num_same / len(ground_truth_tokens)
        f1 = (2 * precision * recall) / (precision + recall)
        max_f1 = max(f1, max_f1)  # choose maximum f1 value among multiple gold answers
    
    return max_f1


def calculate_em(prediction, gold_list):
    em = 0
    cover_em = 0
    prediction = normalize_answer(prediction)
    
    for gold in gold_list:
        gold = normalize_answer(gold)
        if prediction == gold:
            return 1, 1
        elif gold in prediction:
            cover_em += 1
    
    return int(em > 0), int(cover_em > 0)
    

def main(predictions_file_path):
    total_entries = 0
    em = 0
    cover_em = 0
    f1 = 0.0
    with open(predictions_file_path, 'r') as file:
        for line in file:
            entry = json.loads(line.strip())
            
            gold_answers = entry['gold']
            predicted = entry['predicted'].lower().strip()
            
            cur_em, cur_cover_em = calculate_em(predicted, gold_answers)
            cur_f1 = calculate_f1(predicted, gold_answers)
            
            em += cur_em
            cover_em += cur_cover_em
            f1 += cur_f1
                
            total_entries += 1

    print("******* Results *******")
    print("Num Total Entries:", total_entries)
    print("EM:", em / total_entries)  
    print("Cover EM:", cover_em / total_entries)
    print("F1:", f1 / total_entries)


if __name__ == "__main__":
    # TODO: change to your own path
    predictions_file_path = '../results/hotpotqa_test_500_predictions.jsonl'
    main(predictions_file_path)
    