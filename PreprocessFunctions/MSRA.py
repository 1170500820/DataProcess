# coding:utf-8
import json
import os
from utils import *

dataset_name = 'MSRA/'
dataset_prefix = ''

PROCESS_FILES = [
    'msra_test_bio.txt',
    'msra_train_bio.txt'
]
OUTPUT_NAMES = {
    'msra_test_bio.txt': 'test.json',
    'msra_train_bio.txt': 'train.json'
}


def conllner_to_lst(filepath: str) -> List[Dict[str, Any]]:
    """
    输入文件路径，读取其中的数据，每个sample转化为一个dict
    包含的keys：
        - chars
        - tags
        - id

    conll每个sample的格式类似于这样

    # id a23618fa-10ec-4f5e-bed2-682879bfb054	domain=mix
    华 _ _ O
    盛 _ _ O
    顿 _ _ O
    maynard _ _ B-LOC
    天 _ _ O
    气 _ _ O

    华 O
    盛 O
    顿 O
    maynard B-LOC
    天 O
    气 O

    (两种格式都能够处理)

    不同sample之间用两个\n进行分割
    :param filepath: Conll训练文件的路径
    :return:
    """
    lines = open(filepath, 'r', encoding='utf-8').read().strip().split('\n\n')
    dict_lst = []
    for elem_sample in lines:
        elem_sample = elem_sample.strip()  # 有时会遇到三个\n
        sample = {}
        sents = elem_sample.split('\n')
        if sents[0][0] == '#':
            info, taggings = sents[0], sents[1:]

            # id
            info_detail = info.split('\t')
            sample['id'] = info_detail[0].split()[-1]
        else:
            taggings = sents

        # tokens and tags
        sample['chars'], sample['tags'] = [], []
        for elem_tagging in taggings:
            elem_tagging_split = elem_tagging.split()
            cur_token, cur_tagging = elem_tagging_split[0], elem_tagging_split[-1]
            sample['chars'].append(cur_token)
            sample['tags'].append(cur_tagging)

        dict_lst.append(sample)

    return dict_lst


def conllner_weibo_to_lst(filepath: str) -> List[Dict[str, Any]]:
    """
    输入文件路径，读取其中的数据，每个sample转化为一个dict
    包含的keys：
        - chars
        - tags
        - seg
    专门为weibo的NER数据提供
    weibo的数据会在char后面加入0和1来表示分词信息，本函数在conllner_to_lst的基础上将分词隔离出来而已
    :param filepath:
    :return:
    """
    dict_lst = conllner_to_lst(filepath)
    new_dict_lst = []
    for elem_d in dict_lst:
        chars = elem_d['chars']
        real_chars, seg = [], []
        for elem_char in chars:
            real_chars.append(elem_char[:-1])
            seg.append(elem_char[-1])
        new_dict_lst.append({
            "seg": seg,
            "chars": real_chars,
            "tags": elem_d['tags']
        })
    return new_dict_lst


def check_BIO_string(BIO_string: List[str]):
    """
    检查一个BIO的strlist是否合法。如果合法，则直接返回。否则报错

    - 长度为0是合法的
    - I-type前面要么是B-type，要么是I-type，否则非法
    :param BIO_string:
    :return:
    """
    if len(BIO_string) == 0:
        return
    last = 'O'
    for idx, elem in enumerate(BIO_string):
        if elem[0] == 'I':
            if last == 'B' + elem[1:] or last == elem:
                last = elem
                continue
            else:
                raise Exception(f'[check_BIO_string]非法的I位置:{idx}！')
        last = elem
    return


def BIO_to_spandict(BIO_string: List[str]) -> Dict[str, List[Tuple[int, int]]]:
    """
    将BIO格式标注，转化为span的dict。
    不会检查BIO_string合法性。如果BIO_string存在非法标注，抛出异常

    其中BIO格式：
        如果词长为1，则为B-type
        词长>=2，则为 B-type, I-type, ...
        否则为O

    span格式：
        第一个字的坐标为0
        start为该词第一个字的坐标
        end为该词右侧的第一个字的坐标
    :param BIO_string:
    :return:
    """
    check_BIO_string(BIO_string)
    tag_types = list(set(x[2:] for x in set(BIO_string) - {'O'}))
    spandict = {x: [] for x in tag_types}  # Dict[type name, list of span tuple]

    # 根据每一个tag以及其上一个tag，判断该tag是否是标注内
    # 外->内 内作为start ,内->外 外作为end
    # 例外，若最后一个仍在标注内，end=len(BIO_string)
    last_tag = 'O'
    span_list = []
    for idx, tag in enumerate(BIO_string):
        if tag[0] == 'B':
            if last_tag[0] != 'O':
                span_list.append(idx)
                cur_tag_type = last_tag[2:]
                spandict[cur_tag_type].append(tuple(span_list))
                span_list = []
            span_list.append(idx)
            last_tag = tag
            continue
        elif last_tag != 'O' and tag[0] == 'O':
            span_list.append(idx)
            cur_tag_type = last_tag[2:]
            spandict[cur_tag_type].append(tuple(span_list))
            span_list = []
        last_tag = tag
    if len(span_list) == 1:
        span_list.append(len(BIO_string))
        cur_tag_type = last_tag[2:]
        spandict[cur_tag_type].append(tuple(span_list))
        span_list = []

    return spandict


def process_(dataset_path: str, output_path: str):
    create_new_dir_if_not_exist(os.path.join(output_path, dataset_name))
    for elem_path in PROCESS_FILES:
        d = conllner_to_lst(os.path.join(dataset_path, dataset_prefix, elem_path))
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
        output_name = OUTPUT_NAMES[elem_path] if elem_path in OUTPUT_NAMES else elem_path
        dump_jsonl(results, os.path.join(output_path, dataset_name, output_name))
