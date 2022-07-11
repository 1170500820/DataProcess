# coding:utf-8
import json
import os
from utils import *

dataset_name = 'ASAP/'
dataset_prefix1 = 'ASAP/ASAP_SENT/'
dataset_prefix2 = 'ASAP/ASAP_ASPECT/'

PROCESS_FILES = [
    'dev.tsv',
    'train.tsv',

]
OUTPUT_NAMES = {
    'dev.tsv': 'dev.json',
    'train.tsv': 'train.json',
}


def process_(dataset_path: str, output_path: str):

    create_new_dir_if_not_exist(os.path.join(output_path, 'ASAP.ASAP_SENT'))
    create_new_dir_if_not_exist(os.path.join(output_path, 'ASAP.ASAP_ASPECT'))

    for elem_path in PROCESS_FILES:
        d = load_tsv(os.path.join(dataset_path, dataset_prefix1, elem_path))
        output_name = OUTPUT_NAMES[elem_path] if elem_path in OUTPUT_NAMES else elem_path
        dump_jsonl(d, os.path.join(output_path, 'ASAP.ASAP_SENT', output_name))
    for elem_path in PROCESS_FILES:
        d = load_tsv(os.path.join(dataset_path, dataset_prefix2, elem_path))
        output_name = OUTPUT_NAMES[elem_path] if elem_path in OUTPUT_NAMES else elem_path
        dump_jsonl(d, os.path.join(output_path, 'ASAP.ASAP_ASPECT', output_name))
