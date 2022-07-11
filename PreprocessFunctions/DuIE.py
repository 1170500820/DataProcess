# coding:utf-8
import json
import os
from utils import *

dataset_name = 'DuIE/'
dataset_prefix = 'DuIE2.0/'

PROCESS_FILES = [
    'duie_dev.json/duie_dev.json',
    'duie_train.json/duie_train.json',
]
OUTPUT_NAMES = {
    'duie_dev.json/duie_dev.json': 'dev.json',
    'duie_train.json/duie_train.json': 'train.json',
}


def process_(dataset_path: str, output_path: str):
    create_new_dir_if_not_exist(os.path.join(output_path, dataset_name))
    for elem_path in PROCESS_FILES:
        d = load_jsonl(os.path.join(dataset_path, dataset_prefix, elem_path))
        output_name = OUTPUT_NAMES[elem_path] if elem_path in OUTPUT_NAMES else elem_path
        dump_jsonl(d, os.path.join(output_path, dataset_name, output_name))
