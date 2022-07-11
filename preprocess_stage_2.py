"""
第二阶段的预处理，会把数据集进行拆分重组，取其中需要的内容，使其能够构成instruction + text -> answer 的形式
- 一个数据集可能（大多数情况下）生成多个子数据集
"""
import os
from loguru import logger
from settings import *
from PreprocessFunctions2 import \
    MSRA

use_test = False

dataset2function = {
    'MSRA': MSRA.process_
}
unavailable_dataset = {}


def preprocess():
    logger.info('对数据集机械能第二阶段处理，该阶段处理完成的数据将用于prompt生成')
    all_dataset = dataset2function.keys()
    available_dataset = list(x for x in all_dataset if x not in unavailable_dataset)
    logger.info(f'需要处理的数据集：{",".join(available_dataset)}')

    for e_dataset_name in available_dataset:
        if e_dataset_name in unavailable_dataset:
            continue
        logger.info(f'正在处理：{e_dataset_name}')
        dataset2function[e_dataset_name](os.path.join(stage1_processed_path, e_dataset_name), stage2_processed_path, use_test)


if __name__ == '__main__':
    preprocess()
