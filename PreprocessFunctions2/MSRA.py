# coding:utf-8
import json
import os
from utils import *
import random

dataset_name = 'MSRA'

tag2name = {
    'LOC': '地点',
    'PER': '人物',
    'ORG': '组织'
}

PROCESS_FILES = [
    'train.json', 'test.json', 'dev.json'
]


def process1(sample: dict) -> list:
    """
    按类型对实体类型进行询问，每个数据只询问一个类型
    :param sample:
    :return:
    """
    results = []
    text = sample['text']
    ners = sample['ners']
    for key, value in ners.items():
        ner_type = tag2name[key]
        results.append({
            'text': text,
            'ner_type': ner_type,
            'entities': value
        })
    return results


def process2(sample: dict) -> list:
    """
    已知一个实体，然后去抽取剩下的
    :param sample:
    :return:
    """
    results = []
    text = sample['text']
    ners = sample['ners']
    for key, value in ners.items():
        if len(value) < 2:
            continue
        ner_type = tag2name[key]
        rand_pick = random.randint(0, len(value) - 1)
        pick_ner = value[rand_pick]
        other_ner = value[0: rand_pick] + value[rand_pick + 1:]
        results.append({
            'text': text,
            'ner_type': ner_type,
            'picked_entity': pick_ner,
            'other_entities': other_ner
        })
    return results


subsets = {
    'ParticularType': process1,
    'OneForTheOther': process2
}


def process_(dataset_path: str, output_path: str, use_test: bool = False):
    for subset in subsets.keys():
        subset_filename = f'{dataset_name}.{subset}'
        create_new_dir_if_not_exist(os.path.join(output_path, subset_filename))
        for elem_path in PROCESS_FILES:
            if not use_test and elem_path == 'test.json':
                continue
            if not os.path.exists(os.path.join(dataset_path, elem_path)):
                continue
            d = load_jsonl(os.path.join(dataset_path, elem_path))
            processed = []
            for elem in d:
                processed.extend(subsets[subset](elem))
            dump_jsonl(processed, os.path.join(output_path, subset_filename, elem_path))
