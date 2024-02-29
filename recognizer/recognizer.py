import json
import threading
import time

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from Tools import QrcodeMaker


class Recognizer(object):
    __result_dict = {}
    __Recognizers = []
    __NextRecognizer = 0
    __RecognizerCode = 0

    __NowRecognizer = 0

    def __init__(self):
        pass

    @staticmethod
    def AddResult(result: str, code: str):
        if code not in Recognizer.__result_dict:
            Recognizer.__result_dict[code] = []

        Recognizer.__result_dict[code].append(result)

        data = Recognizer.__result_dict[code]
        return data

    @staticmethod
    def DeleteResult(code: str):
        data = Recognizer.__result_dict[code]
        del Recognizer.__result_dict[code]
        return data

    @staticmethod
    def Add(code):
        Recognizer.__Recognizers.append(code)

    @staticmethod
    def remove(code):
        Recognizer.__Recognizers.remove(code)

    @staticmethod
    def GetNewRecognizerCode() -> str:
        code = 1
        while True:
            if str(code) in Recognizer.__Recognizers:
                code += 1
                continue
            break

        code = str(code)
        Recognizer.Add(code)

        return code

    @staticmethod
    def SendDelData(code):
        data = {
            'action': "delete",
            'code': code
        }
        background_thread = threading.Thread(target=Recognizer.SendMessage, args=(data,))
        background_thread.start()

    @staticmethod
    def SendMessage(Msg: str):
        channel_layer = get_channel_layer()
        data = json.dumps(Msg)
        time.sleep(2)
        param = {
            "type": "send_message",
            "data": data
        }
        async_to_sync(channel_layer.group_send)('Recognizer', param)
