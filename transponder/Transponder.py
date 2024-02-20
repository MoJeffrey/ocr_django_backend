import logging

import requests

from generators.enum.ActionEnum import ActionEnum
from ocr_django.settings import Transponder_URL


class Transponder:
    url: str = None
    headers: dict = None
    method: str = None
    data: dict = None
    params: dict = None
    code: str = None

    def __init__(self, Object: dict):
        self.__dict__ = Object.copy()

    def Run(self):
        URL = Transponder_URL + self.url

        logging.info(URL)
        if self.method == 'POST':
            response = requests.post(url=URL, headers=self.headers, json=self.data, params=self.params)
        else:
            response = requests.get(url=URL, headers=self.headers, data=self.data, params=self.params)
        data = response.json()

        logging.info(data)
        return data

    def GetData(self):
        return {
            'action': ActionEnum.answer.value,
            'data': self.Run(),
            'code': self.code
        }
