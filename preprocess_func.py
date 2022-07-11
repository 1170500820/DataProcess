from settings import *
import json
from tqdm import tqdm
import os


def process_ChFinAnn(dataset_path: str, output_path: str):
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
            events_of_current_sample.append([[elem_event_type], elem_event_arg_types, elem_event_args])

        sample = {
            "sentences": sentences,
            "events": events_of_current_sample
        }
        return sample
    prefix = 'Data/'

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
        'EndDate', 'LaterHoldingShares', 'RepurchasedShares', 'LowestTradingPrice', 'EquityHolder',
        'TotalPledgedShares', 'RepurchaseAmount', 'TradedShares', 'Pledger', 'Pledgee', 'CompanyName',
        'HighestTradingPrice', 'StockAbbr', 'ReleasedDate', 'OtherType', 'PledgedShares', 'TotalHoldingRatio',
        'AveragePrice', 'UnfrozeDate', 'FrozeShares', 'StockCode', 'TotalHoldingShares'}

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

    for elem_path in PROECESS_FILES:
        d = json.load(open(os.path.join(dataset_path, prefix, elem_path), 'r', encoding='utf-8'))