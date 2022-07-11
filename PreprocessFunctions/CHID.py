# coding:utf-8
import json
import os
import re
from utils import *

dataset_name = 'CHID/'
dataset_prefix = ''

PROCESS_FILES = [
    'train.json',
    'dev.json'
]
OUTPUT_NAMES = {
}


def p(dataset_path: str, elem_path: str):
    datas = list(json.loads(x) for x in open(os.path.join(dataset_path, dataset_prefix, elem_path), 'r', encoding='utf-8').read().strip().split('\n'))
    data_answers = json.load(open(os.path.join(dataset_path, dataset_prefix, elem_path.split('.')[0] + '_answer.' + elem_path.split('.')[1]), 'r', encoding='utf-8'))
    data_exp = json.load(open(os.path.join(dataset_path, dataset_prefix, 'idiomDict.json'), 'r', encoding='utf-8'))
    processed = []
    for elem_data in datas:
        candidates = elem_data['candidates']
        contents = elem_data['content']

        for elem_content in contents:
            idiom_tags = re.findall(r'#idiom\d{6}#', elem_content)  # StrList
            indexes = list(data_answers[x] for x in idiom_tags)  # IntList
            # 按顺序列举该句子中需要填空的成语
            idioms = list(candidates[x] for x in indexes)  # List[idiom]
            # 候选成语的解释
            explanations = []
            for elem_key in candidates:
                explanations.append([elem_key, data_exp[elem_key]])
            modified_content = re.sub(r'#idiom\d{6}#', '____', elem_content)
            processed.append({
                "candidates": candidates,
                "content": modified_content,
                "explanations": explanations,
                "answers": idioms
            })
    return processed


def process_(dataset_path: str, output_path: str):
    create_new_dir_if_not_exist(os.path.join(output_path, dataset_name))
    for elem_path in PROCESS_FILES:
        processed = p(dataset_path, elem_path)
        output_name = OUTPUT_NAMES[elem_path] if elem_path in OUTPUT_NAMES else elem_path
        dump_jsonl(processed, os.path.join(output_path, dataset_name, output_name))
