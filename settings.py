from typing import *


origin_data_path = r'../ChineseDatasetCollection/'
stage1_processed_path = r'../Stage1PreprocessedDataset/'
stage2_processed_path = r'../Stage2PreprocessedDataset/'

dataset_list = [
    'CEC', 'CEEC', 'DuEE', 'ChFinAnn', 'DuReader_robust', 'DuReader_checklist',
    'DuReader_yesno', 'DuIE_2.0', 'DuEE-fin', 'AdvertiseGen', 'LCSTS_new', 'LCQMC',
    'BQ', 'PAES-X', 'ASAP', 'SE-ABSA_16', 'NLPCC14-SC', 'DUEL_2.0', 
    'ChnSentiCorp', 'LUGE-Dialogue', 'DuQM', 'OPPO小布对话文本语义匹配', '微博开放域文本对话', '豆瓣中文开放域对话',
    'LCCC', '腾讯中文开放域对话', 'ESTC'
]

dataset2path = {
    'CEC': 'CEC-Corpus-master',
    'CEEC': 'CEEC-Corpus-master',
    'ChFinAnn': 'ChFinAnn'
}