# coding:utf-8
import json
import os
from utils import *

dataset_name = 'LCQMC/'
dataset_prefix = 'lcqmc/'

PROCESS_FILES = [
    'dev.tsv',
    'train.tsv',
]
OUTPUT_NAMES = {
    'dev.tsv': 'dev.json',
    'train.tsv': 'train.json',
}


def process_(dataset_path: str, output_path: str):
    create_new_dir_if_not_exist(os.path.join(output_path, dataset_name))
    for elem_path in PROCESS_FILES:
        d = load_tsv(os.path.join(dataset_path, dataset_prefix, elem_path), first_line_tag=False)

        processed = list({'sentence1': x[0], 'sentence2': x[1], 'is_similar': True if x[2] == '1' else False} for x in d)
        output_name = OUTPUT_NAMES[elem_path] if elem_path in OUTPUT_NAMES else elem_path
        dump_jsonl(processed, os.path.join(output_path, dataset_name, output_name))
