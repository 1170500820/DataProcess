# coding:utf-8
import json
import os
from utils import *

dataset_name = 'DuEE_fin/'
dataset_prefix = 'DuEE-fin'

PROCESS_FILES = [
    'duee_fin_dev.json/duee_fin_dev.json',
    'duee_fin_train.json/duee_fin_train.json'
]
OUTPUT_NAMES = {
    'duee_fin_dev.json/duee_fin_dev.json': 'dev.json',
    'duee_fin_train.json/duee_fin_train.json': 'train.json'
}


def process_(dataset_path: str, output_path: str):
    create_new_dir_if_not_exist(os.path.join(output_path, dataset_name))
    for elem_path in PROCESS_FILES:
        d = load_jsonl(os.path.join(dataset_path, dataset_prefix, elem_path))
        output_name = OUTPUT_NAMES[elem_path] if elem_path in OUTPUT_NAMES else elem_path
        dump_jsonl(d, os.path.join(output_path, dataset_name, output_name))
