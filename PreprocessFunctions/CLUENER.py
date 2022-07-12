# coding:utf-8
import json
import os
from utils import *

dataset_name = 'CLUENER/'
dataset_prefix = ''


tag2chinese = {
    'address': '地址',
    'book': '书名',
    'company': '公司',
    'game': '游戏',
    'government': '政府',
    'movie': '电影',
    'name': '姓名',
    'organization': '组织机构',
    'position': '职位',
    'scene': '景点'
}


PROCESS_FILES = [
    'dev.json',
    'train.json'
]
OUTPUT_NAMES = {
}


def process_sample(d: dict):
    text = d['text']
    ners = {}
    for key, value in d['label'].items():
        # ner_tag = tag2chinese[key]
        words = list(value.keys())
        ners[key] = words
    return {
        'text': text,
        'ners': ners
    }


def process_(dataset_path: str, output_path: str):
    create_new_dir_if_not_exist(os.path.join(output_path, dataset_name))
    for elem_path in PROCESS_FILES:
        d = load_jsonl(os.path.join(dataset_path, dataset_prefix, elem_path))
        processed = list(process_sample(x) for x in d)
        output_name = OUTPUT_NAMES[elem_path] if elem_path in OUTPUT_NAMES else elem_path
        dump_jsonl(processed, os.path.join(output_path, dataset_name, output_name))
