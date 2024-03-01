import logging
import re


class QRCodeDataDTO:
    code = None
    data_all_num = None
    curr_num = None
    result: str = None

    def __init__(self, result):
        self.result = result
        self.identify()

    def identify(self):
        self.code = re.search(r'[QACE]\d+', self.result).group()
        self.data_all_num = int(re.search(r'\[[AQCE]\d+_\d+_(\d+)]', self.result).group(1))
        self.curr_num = int(re.search(r'\[[AQCE]\d+_(\d+)_\d+]', self.result).group(1))

    @staticmethod
    def splicing(current_data_list: list) -> str:
        sorted_data = sorted(current_data_list, key=lambda x: int(re.search(r'\[[AQCE]\d+_(\d+)_\d+]', x).group(1)))
        return ''.join([d[d.index(']') + 1:] for d in sorted_data])
