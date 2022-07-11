import json
import os

from utils import *


dataset_name = 'DuEE/'
dataset_prefix = 'DuEE1.0/'

PROECESS_FILES = [
    'duee_train.json/duee_train.json',
    'duee_dev.json/duee_dev.json'
]
OUTPUT_NAMES = {
    'duee_train.json/duee_train.json': 'train.json',
    'duee_dev.json/duee_dev.json': 'dev.json'
}


def process_DuEE(dataset_path: str, output_path: str):
    create_new_dir_if_not_exist(os.path.join(output_path, dataset_name))
    for elem_path in PROECESS_FILES:
        d = load_jsonl(os.path.join(dataset_path, dataset_prefix, elem_path))
        output_name = OUTPUT_NAMES[elem_path] if elem_path in OUTPUT_NAMES else elem_path
        dump_jsonl(d, os.path.join(output_path, dataset_name, output_name))
