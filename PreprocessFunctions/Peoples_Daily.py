# coding:utf-8
import json
import os
from utils import *
from PreprocessFunctions.MSRA import conllner_to_lst, BIO_to_spandict

dataset_name = 'Peoples_Daily/'
dataset_prefix = ''

PROCESS_FILES = [
    'example.dev',
    'example.test',
    'example.train'
]
OUTPUT_NAMES = {
    'example.dev': 'dev.json',
    'example.test': 'test.json',
    'example.train': 'train.json'
}


def postprocess(filepath: str):
    d = conllner_to_lst(filepath)
    results = []
    for idx in range(len(d)):
        tag_dict = BIO_to_spandict(d[idx]['tags'])
        text = ''.join(d[idx]['chars'])
        ners = {}
        for key, value in tag_dict.items():
            ners[key] = []
            for elem_span in value:
                ners[key].append(text[elem_span[0]: elem_span[1]])
        results.append({
            'text': text,
            'tag_dict': tag_dict,
            'ners': ners
        })
    return results


def process_(dataset_path: str, output_path: str):
    create_new_dir_if_not_exist(os.path.join(output_path, dataset_name))
    for elem_path in PROCESS_FILES:
        processed = postprocess(os.path.join(dataset_path, dataset_prefix, elem_path))
        output_name = OUTPUT_NAMES[elem_path] if elem_path in OUTPUT_NAMES else elem_path
        dump_jsonl(processed, os.path.join(output_path, dataset_name, output_name))
