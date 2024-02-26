import logging

import requests

from generators.enum.ActionEnum import ActionEnum
from ocr_django.settings import Transponder_URL
from recognizer.DTO.RecognizerDTO import RecognizerDTO


class Transponder:
    url: str = None
    headers: dict = None
    method: str = None
    data: dict = None
    params: dict = None

    def __init__(self, Object: dict = None):
        if Object is not None:
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

    def GetData(self) -> dict:
        return {
            "url": self.url,
            "method": self.method,
            "data": self.data,
            "params": self.params,
            "headers": self.headers,
        }
