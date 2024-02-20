import json
import logging

from channels.generic.websocket import AsyncWebsocketConsumer

from generators import Generator
from generators.enum.ActionEnum import ActionEnum
from recognizer.recognizer import Recognizer
from transponder.Transponder import Transponder


class RecognizerWebSocket(AsyncWebsocketConsumer):
    __RecognizerCode = None

    async def connect(self):
        self.__RecognizerCode = Recognizer.GetNewRecognizerCode()
        await self.channel_layer.group_add(self.__RecognizerCode, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        Recognizer.remove(self.__RecognizerCode)
        await self.channel_layer.group_discard(self.__RecognizerCode, self.channel_name)

    async def receive(self, text_data: str = None, bytes_data: str = None):
        try:
            data = json.loads(text_data)
            if data['action'] == ActionEnum.transponder.value:
                logging.info("收到问题")
                transponder = Transponder(data)
                await Generator.Run(transponder.GetData(), isQuestion=False, code=transponder.code)
            elif data['action'] == ActionEnum.answer.value:
                Generator.SetAnswer(data)
                logging.info("收到答案")
        except Exception as e:
            pass
