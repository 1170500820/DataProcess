# coding:utf-8
import json
import os
from utils import *
import settings

dataset_name = 'OPPO小布对话文本语义匹配/'
dataset_prefix = ''

PROCESS_FILES = [
    'oppp.json'
]
OUTPUT_NAMES = {
}


def process_(dataset_path: str, output_path: str):
    create_new_dir_if_not_exist(os.path.join(output_path, dataset_name))
    d = json.load(open(os.path.join(settings.origin_data_path, dataset_name, dataset_prefix, PROCESS_FILES[0]), 'r', encoding='utf-8'))
    for subset in ['train', 'dev']:
        subd = d[subset]
        dump_jsonl(subd, os.path.join(output_path, dataset_name, f'{subset}.json'))

