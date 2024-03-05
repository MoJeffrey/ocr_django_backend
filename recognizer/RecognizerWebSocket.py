import logging
import traceback

from channels.generic.websocket import AsyncWebsocketConsumer

from generators.generators import Generator
from generators.enum.ActionEnum import ActionEnum
from recognizer.DTO.QRCodeDataDTO import QRCodeDataDTO
from recognizer.DTO.RecognizerDTO import RecognizerDTO
from recognizer.recognizer import Recognizer
from transponder.Transponder import Transponder


class RecognizerWebSocket(AsyncWebsocketConsumer):
    __GroupName = 'Recognizer'
    __RecognizerCode = None

    async def connect(self):
        self.__RecognizerCode = Recognizer.GetNewRecognizerCode()
        try:
            await self.channel_layer.group_add(self.__GroupName, self.channel_name)
        except Exception:
            logging.error(traceback.print_exc())
            Recognizer.remove(self.__RecognizerCode)
            return
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
        data = QRCodeDataDTO(text_data)
        current_data = Recognizer.AddResult(text_data, data.code)

        if len(current_data) != data.data_all_num:
            return

        data = QRCodeDataDTO.splicing(current_data)
        DTD = RecognizerDTO(StringObj=data)
        await RecognizerWebSocket.Run(DTD)

    @staticmethod
    async def Run(data: RecognizerDTO):
        try:
            if data.action == ActionEnum.transponder.value:
                transponder = Transponder(data.data)
                await Generator.Run(transponder.GetRecognizerDTO(data.code), isQuestion=False, code=data.code)
            elif data.action == ActionEnum.answer.value:
                Generator.SetAnswer(data)
            elif data.action == ActionEnum.close.value:
                await Generator.ToCloseAnswer(data.code)
            elif data.action == ActionEnum.end.value:
                await Generator.ToEndQuestion(data.code)

        except Exception as e:
            logging.error(traceback.print_exc())
            logging.error(e)
            logging.error(data.action)
            logging.error(data.code)

    async def send_message(self, event):
        data = event['data']
        await self.send(text_data=data)
