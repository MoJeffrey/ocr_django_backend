import logging

from channels.generic.websocket import AsyncWebsocketConsumer

from generators.generators import Generator
from generators.enum.ActionEnum import ActionEnum
from recognizer.DTO.RecognizerDTO import RecognizerDTO
from recognizer.recognizer import Recognizer
from transponder.Transponder import Transponder


class RecognizerWebSocket(AsyncWebsocketConsumer):
    __GroupName = 'Recognizer'
    __RecognizerCode = None

    async def connect(self):
        self.__RecognizerCode = Recognizer.GetNewRecognizerCode()
        await self.channel_layer.group_add(self.__GroupName, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        Recognizer.remove(self.__RecognizerCode)
        await self.channel_layer.group_discard(self.__GroupName, self.channel_name)

    async def receive(self, text_data: str = None, bytes_data: str = None):
        """
        收到识别器的信息
        :param text_data:
        :param bytes_data:
        :return:
        """
        try:
            DTD = RecognizerDTO(StringObj=text_data)

            if DTD.action == ActionEnum.transponder.value:
                transponder = Transponder(DTD.data)

                NewDTO = RecognizerDTO()
                NewDTO.action = ActionEnum.answer.value
                NewDTO.data = transponder.Run()
                NewDTO.code = DTD.code.replace('A', 'Q')

                await Generator.Run(NewDTO.GetData(), isQuestion=False, code=DTD.code)
            elif DTD.action == ActionEnum.answer.value:
                Generator.SetAnswer(DTD)
            elif DTD.action == ActionEnum.close.value:
                await Generator.ToCloseAnswer(DTD.code)

        except Exception as e:
            logging.error(e)

    async def send_message(self, event):
        data = event['data']
        await self.send(text_data=data)
