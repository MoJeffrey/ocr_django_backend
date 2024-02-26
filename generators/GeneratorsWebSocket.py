import json

from channels.generic.websocket import AsyncWebsocketConsumer
from generators.enum.GeneratorsWebSocketMethodEnum import GeneratorsWebSocketMethodEnum
from generators.generators import Generator


class GeneratorsWebSocket(AsyncWebsocketConsumer):
    __GroupName = 'Generator'
    __GeneratorCode: str = None

    async def connect(self):
        self.__GeneratorCode = Generator.GetNewGeneratorCode()
        await self.channel_layer.group_add(self.__GroupName, self.channel_name)
        await self.accept()

        data = {
            "method": GeneratorsWebSocketMethodEnum.authorization.value,
            "code": self.__GeneratorCode
        }
        await self.send(text_data=json.dumps(data))

    async def disconnect(self, close_code):
        Generator.remove(self.__GeneratorCode)
        await self.channel_layer.group_discard(self.__GroupName, self.channel_name)

    async def receive(self, text_data: dict = None, bytes_data: str = None):
        await self.send(text_data=json.dumps(text_data['data']))
