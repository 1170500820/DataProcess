# coding:utf-8
import json
import os
from utils import *

dataset_name = 'DuReader_robust/'
dataset_prefix = 'dureader_robust-data'

PROCESS_FILES = [
    'test.json',
    'train.json',
    'dev.json'
]
OUTPUT_NAMES = {
}


def process_(dataset_path: str, output_path: str):
    create_new_dir_if_not_exist(os.path.join(output_path, dataset_name))
    for elem_path in PROCESS_FILES:
        d = load_json(os.path.join(dataset_path, dataset_prefix, elem_path), key='data')[0]['paragraphs']
        output_name = OUTPUT_NAMES[elem_path] if elem_path in OUTPUT_NAMES else elem_path
        dump_jsonl(d, os.path.join(output_path, dataset_name, output_name))
