import json

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from Tools import QrcodeMaker


class Recognizer(object):
    __Recognizers = []
    __NextRecognizer = 0
    __RecognizerCode = 0

    __NowRecognizer = 0

    def __init__(self):
        pass

    @staticmethod
    def GetRecognizer() -> str:
        RecognizerCode = Recognizer.__Recognizers[Recognizer.__NextRecognizer]
        Recognizer.__NextRecognizer += 1
        if Recognizer.__NextRecognizer == Recognizer.__NowRecognizer:
            Recognizer.__NextRecognizer = 0
        return RecognizerCode

    @staticmethod
    def Get() -> str:
        pass

    @staticmethod
    def Add(code):
        Recognizer.__Recognizers.append(code)
        Recognizer.__NowRecognizer += 1
        Recognizer.Get = Recognizer.GetRecognizer

    @staticmethod
    def remove(code):
        Recognizer.__Recognizers.remove(code)
        Recognizer.__NowRecognizer -= 1

    @staticmethod
    def GetNewRecognizerCode() -> str:
        Recognizer.__RecognizerCode += 1
        Code = f'Recognizer_{Recognizer.__RecognizerCode}'
        Recognizer.Add(Code)

        return Code
