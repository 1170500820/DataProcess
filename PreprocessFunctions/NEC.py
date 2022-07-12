# coding:utf-8
import json
import os
from utils import *

dataset_name = 'NEC/'
dataset_prefix = ''

PROCESS_FILES = [
    'dev.json',
    'train.json'
]
OUTPUT_NAMES = {
    'dev.json': 'NEC.dev/dev.json',
    'train.json': 'NEC.train/train.json'
}


def process_(dataset_path: str, output_path: str):
    create_new_dir_if_not_exist(os.path.join(output_path, f'{dataset_name[:-1]}.dev'))
    create_new_dir_if_not_exist(os.path.join(output_path, f'{dataset_name[:-1]}.train'))
    for elem_path in PROCESS_FILES:
        d = load_jsonl(os.path.join(dataset_path, dataset_prefix, elem_path))
        output_name = OUTPUT_NAMES[elem_path] if elem_path in OUTPUT_NAMES else elem_path
        dump_jsonl(d, os.path.join(output_path, output_name))
