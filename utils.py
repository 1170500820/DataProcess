from settings import *
import os
import json
from rich.console import Console
from rich.table import Column, Table


"""
统计与采样
"""


def count_stage1_dataset(dataset_name: str):
    """

    :param dataset_name:
    :return:
    """
    dataset_dir = os.path.join(stage1_processed_path, dataset_name)
    subsets = ['train', 'test', 'dev']
    count = {}
    for elem in subsets:
        if os.path.exists(os.path.join(dataset_dir, elem + '.json')):
            d = load_jsonl(os.path.join(dataset_dir, elem + '.json'))
            count[elem] = len(d)
    return count


def show_all_stage1_dataset():
    dataset_names = os.listdir(stage1_processed_path)
    counts = {}
    for elem in dataset_names:
        elem_count = count_stage1_dataset(elem)
        elem_count['total'] = sum(elem_count.values())
        counts[elem] = elem_count

    draw_count(counts)




def sample_raw_data(dataset_names: List[str]):
    pass


def sample_prompted_data(prompted_dataset_names: List[str]):
    pass


"""
目录与文件操作
"""


def create_new_dir_if_not_exist(path_name: str):
    """
    如果目录不存在，则创建新目录
    :param path_name:
    :return:
    """
    if os.path.isdir(path_name):
        return
    else:
        os.mkdir(path_name)
        return


def load_jsonl(datapath: str):
    d = list(json.loads(x) for x in open(datapath, 'r', encoding='utf-8').read().strip().split('\n'))
    return d


def dump_jsonl(data: list, datapath: str):
    f = open(datapath, 'w', encoding='utf-8')
    for elem in data:
        f.write(json.dumps(elem, ensure_ascii=False) + '\n')
    f.close()


def load_json(datapath: str, key: str = None):
    d = json.load(open(datapath, 'r', encoding='utf-8'))
    if key is not None:
        return d[key]
    return d


def load_tsv(datapath: str, first_line_tag: bool = True):
    """

    :param datapath:
    :param first_line_tag: 第一行是否为标签信息
    :return:
    """
    lines = open(datapath, 'r', encoding='utf-8').read().strip().split('\n')
    results = []
    if first_line_tag:
        tags = lines[0].split('\t')
        for elem in lines[1:]:
            parts = elem.split('\t')
            d = {x[0]: x[1] for x in zip(tags, parts)}
            results.append(d)
        return results
    else:
        for elem in lines:
            results.append(elem.split('\t'))
        return results


"""
其他辅助函数
"""


def draw_count(count: dict):
    consle = Console()
    table = Table(show_header=True, header_style='bold magenta')
    table.add_column('Dataset Name', style='dim')
    table.add_column('train count')
    table.add_column('dev count')
    table.add_column('test count')
    table.add_column('total')

    for key, value in count.items():
        table.add_row(
            key,
            str(value['train'] if 'train' in value else 0),
            str(value['dev'] if 'dev' in value else 0),
            str(value['test'] if 'test' in value else 0),
            str(value['total'])
        )
    table.add_row(
        'Total',
        '-',
        '-',
        '-',
        f'{sum(x["total"] for x in count.values())}'
    )
    consle.print(table)


if __name__ == '__main__':
    show_all_stage1_dataset()