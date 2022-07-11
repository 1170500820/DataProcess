#coding:utf-8
"""
该代码处理ChFinAnn数据。
"""
import json
import os
from utils import *

dataset_name = 'ChFinAnn/'
dataset_prefix = 'Data/'

sample_before_process = None

samples_after_process = None

arguments = {
    'TotalHoldingRatio': '总持股比例',
    'TotalHoldingShares': '持有股份总数',
    'LowestTradingPrice': '最低交易价格',
    'TotalPledgedShares': '质押股份总额',
    'AveragePrice': '平均价格',
    'EndDate': '结束日期',
    'PledgedShares': '质押股份',
    'Pledgee': '质权人',
    "Pledger": "质押者",  # 不确定
    'RepurchaseAmount': '回购金额',
    'CompanyName': '公司名',
    'TradedShares': '交易股票',
    'UnfrozeDate': '解冻日期',
    'EquityHolder': "股东",
    'LegalInstitution': '法律制度',
    'StockCode': '股票代码',
    'ClosingDate': '截止日期',  # 不确定
    'StockAbbr': '股票缩写',
    'HighestTradingPrice': '最高交易价格',
    'FrozeShares': '冻结股票',
    'ReleasedDate': '发布日期',  # 不确定
    'LaterHoldingShares': "后期持股",  # 不确定
    'StartDate': "开始日期",
    'RepurchasedShares': "回购股份",
    'OtherType': "其他"}

a = {
    'StartDate',
    'LegalInstitution',
    'ClosingDate',
    'EndDate', 'LaterHoldingShares', 'RepurchasedShares', 'LowestTradingPrice', 'EquityHolder', 'TotalPledgedShares', 'RepurchaseAmount', 'TradedShares', 'Pledger', 'Pledgee', 'CompanyName', 'HighestTradingPrice', 'StockAbbr', 'ReleasedDate', 'OtherType', 'PledgedShares', 'TotalHoldingRatio', 'AveragePrice', 'UnfrozeDate', 'FrozeShares', 'StockCode', 'TotalHoldingShares'}


events = {
    'EquityPledge': "股权出质",
    'EquityUnderweight': "股票减持",
    'EquityFreeze': "股权冻结",
    'EquityRepurchase': "回购",
    'EquityOverweight': "增持"
}

event_types = ["股权出质", "股票减持", "股权冻结", "回购", "增持"]
# 股权出质 ||| 股票减持 ||| 股权冻结 ||| 回购 ||| 增持

PROECESS_FILES = [
    'test.json',
    'train.json',
    'dev.json'
]
OUTPUT_NAMES = {
}


def read_all_arguments():
    """
    读取所有数据集中出现的论元类型
    :return:
    """
    arguments = set()
    for elem_path in PROECESS_FILES:
        d = json.load(open(elem_path, 'r'))
        for elem_event in d:
            infos = elem_event[1]
            fields = infos['ann_mspan2guess_field']
            names = set(fields.values())
            arguments = arguments.union(names)
            event_fields = infos['recguid_eventname_eventdict_list']
            for elem_e in event_fields:
                for elem_arg in elem_e[2].keys():
                    arguments.add(elem_arg)
    return arguments


def read_all_events():
    """
    读取数据集中出现的所有的事件类型
    :return:
    """
    event_names = set()
    for elem_path in PROECESS_FILES:
        d = json.load(open(elem_path, 'r'))
        for elem_event in d:
            infos = elem_event[1]
            events = infos['recguid_eventname_eventdict_list']
            for elem_event_info in events:
                event_names.add(elem_event_info[1])
    return event_names


def process_sample(elem):
    """
    处理一条event数据
    :param elem:
    :return:
    """
    data_id = elem[0]
    data_info = elem[1]
    sentences = data_info['sentences']
    events_of_current_sample = []
    event = data_info['recguid_eventname_eventdict_list']
    for elem_event in event:
        elem_event_type = events[elem_event[1]]
        elem_event_arg_types, elem_event_args = [], []
        for key, value in elem_event[2].items():
            if value is not None:
                elem_event_arg_types.append(arguments[key])
                elem_event_args.append(value)
        arg_dict = {}
        for (arg_type, arg) in zip(elem_event_arg_types, elem_event_args):
            arg_dict[arg_type] = arg
        events_of_current_sample.append({
            'event_type': elem_event_type,
            'arguments': arg_dict
        })
        # events_of_current_sample.append([[elem_event_type], elem_event_arg_types, elem_event_args])

    sample = {
        "sentences": sentences,
        "events": events_of_current_sample
    }
    return sample

def main():
    for elem_path in PROECESS_FILES:
        print(f'正在处理{elem_path}...', end=' ')
        d = json.load(open(elem_path, 'r'))
        processed = list(process_sample(x) for x in d)
        output_name = OUTPUT_NAMES[elem_path] if elem_path in OUTPUT_NAMES else elem_path
        f = open('processed/' + output_name, 'w', encoding='utf-8')
        for elem_p in processed:
            f.write(json.dumps(elem_p, ensure_ascii=False) + '\n')
        # json.dump(processed, open('new_' + elem_path, 'w'), ensure_ascii=False)
        print(f'完成')


def process_ChFinAnn(dataset_path: str, output_path: str):
    create_new_dir_if_not_exist(os.path.join(output_path, dataset_name))
    for elem_path in PROECESS_FILES:
        d = json.load(open(os.path.join(dataset_path, dataset_prefix, elem_path), 'r', encoding='utf-8'))
        processed = list(process_sample(x) for x in d)
        output_name = OUTPUT_NAMES[elem_path] if elem_path in OUTPUT_NAMES else elem_path
        f = open(os.path.join(output_path, dataset_name, output_name), 'w', encoding='utf-8')
        for elem_p in processed:
            f.write(json.dumps(elem_p, ensure_ascii=False) + '\n')
        f.close()


if __name__ == '__main__':
    # d = process_sample(sample_before_process)
    # print(read_all_arguments())
    main()
