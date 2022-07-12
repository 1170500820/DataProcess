# coding:utf-8
import json
import os
from utils import *
import random

dataset_name = 'DuEE'

PROCESS_FILES = [
    'train.json', 'test.json', 'dev.json'
]


def process1(sample: dict) -> list:
    results = []
    text = sample['text']
    for elem_event in sample['event_list']:
        etype = elem_event['event_type']
        etrigger = elem_event['trigger']
        results.append({
            'text': text,
            'event_type': etype,
            'trigger': etrigger
        })
    return results


def process2(sample: dict) -> list:
    results = []
    text = sample['text']
    for elem_event in sample['event_list']:
        etype = elem_event['event_type']
        etrigger = elem_event['trigger']
        for elem_arg in elem_event['arguments']:
            role = elem_arg['role']
            argument = elem_arg['argument']
            results.append({
                'text': text,
                'event_type': etype,
                'trigger': etrigger,
                'role': role,
                'argument': argument
            })
    return results


def process3(sample: dict) -> list:
    results = []
    text = sample['text']
    for elem_event in sample['event_list']:
        etype = elem_event['event_type']
        etrigger = elem_event['trigger']
        arguments = elem_event['arguments']
        if len(arguments) < 2:
            continue
        rand_pick = random.randint(0, len(arguments) - 1)
        pick_arg = arguments[rand_pick]
        other_args = arguments[0: rand_pick] + arguments[rand_pick + 1:]
        results.append({
            'text': text,
            'event_type': etype,
            'trigger': etrigger,
            'picked_arg': pick_arg['argument'],
            'picked_arg_type': pick_arg['role'],
            'other_args': list(x['argument'] for x in other_args),
            'other_arg_types': list(x['role'] for x in other_args)
        })
    return results


def process4(sample: dict) -> list:
    pass


subsets = [{
    'FindTrigger': process1,
    'FindArgWithTrigger': process2,
    'FindArgWithArgs': process3
}]


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
