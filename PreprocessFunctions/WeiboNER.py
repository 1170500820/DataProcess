# coding:utf-8
import json
import os
from utils import *
from PreprocessFunctions.MSRA import conllner_weibo_to_lst, BIO_to_spandict

dataset_name = 'WeiboNER'
dataset_prefix = ''

PROCESS_FILES = [
    'weiboNER_2nd_conll.dev',
    'weiboNER_2nd_conll.test',
    'weiboNER_2nd_conll.train'
]
OUTPUT_NAMES = {
    'weiboNER_2nd_conll.dev': 'dev.json',
    'weiboNER_2nd_conll.test': 'test.json',
    'weiboNER_2nd_conll.train': 'train.json'
}


def postprocess(dicts: List[dict]):
    new_dicts = []
    for elem in dicts:
        text = ''.join(elem['chars'])
        tag_dict = BIO_to_spandict(elem['tags'])
        ners = {}
        for key, value in tag_dict.items():
            ners[key] = []
            for elem_span in value:
                ners[key].append(text[elem_span[0]: elem_span[1]])
        new_dicts.append({
            'text': text,
            'tag_dict': tag_dict,
            'ners': ners
        })
    return new_dicts


def process_(dataset_path: str, output_path: str):
    create_new_dir_if_not_exist(os.path.join(output_path, dataset_name))
    for elem_path in PROCESS_FILES:
        d = conllner_weibo_to_lst(os.path.join(dataset_path, dataset_prefix, elem_path))
        d = postprocess(d)
        output_name = OUTPUT_NAMES[elem_path] if elem_path in OUTPUT_NAMES else elem_path
        dump_jsonl(d, os.path.join(output_path, dataset_name, output_name))


if __name__ == '__main__':
    fname = ''