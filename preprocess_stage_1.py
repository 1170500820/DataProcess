"""
第一阶段的预处理，需要把各个数据集统一转换为train.json, valid.json, test.json
- 如果没有区分，则默认是train.json
- 如果是难以分出sample的，比如语料库，就不处理
"""
import os

from loguru import logger
from settings import *
from PreprocessFunctions import \
    ChFinAnn, \
    DuEE, \
    DuReader_robust, \
    DuIE, \
    AdvertiseGen, \
    LCQMC, \
    ASAP, \
    CHID, \
    CMNLI, \
    MSRA, \
    WeiboNER, \
    Peoples_Daily, \
    DuEE_fin, \
    OPPO, \
    CLUENER, \
    NEC


"""
默认情况下，所有数据集的预处理函数的接口只接收两个参数：原数据集的路径和输出新数据集的根目录
"""
dataset2function = {
    'ChFinAnn': ChFinAnn.process_ChFinAnn,
    'DuEE': DuEE.process_DuEE,
    'DuReader_robust': DuReader_robust.process_,
    'DuIE': DuIE.process_,
    'AdvertiseGen': AdvertiseGen.process_,
    'LCQMC': LCQMC.process_,
    'ASAP': ASAP.process_,
    'CHID': CHID.process_,
    'CMNLI': CMNLI.process_,
    'MSRA': MSRA.process_,
    'WeiboNER': WeiboNER.process_,
    'Peoples_Daily': Peoples_Daily.process_,
    'DuEE_fin': DuEE_fin.process_,
    'OPPO': OPPO.process_,
    'CLUENER': CLUENER.process_,
    'NEC': NEC.process_
}
unavailable_dataset = {'ChFinAnn', 'DuEE', 'DuReader_robust', 'DuIE', 'AdvertiseGen', 'LCQMC', 'ASAP', 'CHID', 'CMNLI',
                       'MSRA', 'DuEE_fin', 'OPPO', }
# unavailable_dataset = {}


def preprocess():
    logger.info('正在对数据集进行第一阶段处理')
    all_dataset = dataset2function.keys()
    available_dataset = list(x for x in all_dataset if x not in unavailable_dataset)
    logger.info(f'需要处理的数据集：{",".join(available_dataset)}')

    for e_dataset_name in available_dataset:
        if e_dataset_name in unavailable_dataset:
            continue
        logger.info(f'正在处理：{e_dataset_name}')
        dataset2function[e_dataset_name](os.path.join(origin_data_path, e_dataset_name), stage1_processed_path)

    logger.info(f'所有数据集的第一阶段预处理已经完成')


if __name__ == '__main__':
    preprocess()
