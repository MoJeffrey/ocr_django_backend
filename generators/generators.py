import json
import time

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django_redis import get_redis_connection

from Tools import QrcodeMaker
from generators.Exceptions.NoGeneratorError import NoGeneratorError
from generators.DTO.QuestionAndAnswerDTO import QuestionAndAnswerDTO
from generators.QuestionAndAnswerEvent import QuestionAndAnswerEvent
from generators.enum.ActionEnum import ActionEnum
from generators.enum.GeneratorsWebSocketMethodEnum import GeneratorsWebSocketMethodEnum


class Generator(object):
    __Generators = []
    __EventList = {}
    __NextGenerator = 0
    __GeneratorCode = 0

    __NowGenerator = 0

    def __init__(self):
        pass

    @staticmethod
    async def GetAnswer(identificationCode: str):
        """
        :param identificationCode:
        :return:
        """
        question: QuestionAndAnswerEvent = Generator.__EventList[identificationCode]
        data = question.getData()
        return data

    @staticmethod
    async def ToClose(identificationCode: str):
        """
        1. 发送删除Question QRcode 图片
        2. 删除QRcode图片
        3. 删除Redis
        :param identificationCode:
        :return:
        """
        question: QuestionAndAnswerEvent = Generator.__EventList[identificationCode]
        param = (question.GeneratorCode, GeneratorsWebSocketMethodEnum.delete.value, question.DTO)
        await Generator.SendWebSocketMessage(*param)

        QrcodeMaker.remove(question.DTO.getDataCodeList())

        del Generator.__EventList[identificationCode]

    @staticmethod
    def ToCloseForTask(identificationCode: str):
        """
        1. 发送删除Question QRcode 图片
        2. 删除QRcode图片
        3. 删除Redis
        :param identificationCode:
        :return:
        """
        question: QuestionAndAnswerEvent = Generator.__EventList[identificationCode]
        param = (question.GeneratorCode, GeneratorsWebSocketMethodEnum.delete.value, question.DTO)
        Generator.SendWebSocketMessageTask(*param)

        QrcodeMaker.remove(question.DTO.getDataCodeList())

        del Generator.__EventList[identificationCode]

    @staticmethod
    def SendWebSocketMessageTask(GeneratorCode: str, method: str, DTO: QuestionAndAnswerDTO):
        channel_layer = get_channel_layer()
        param = {
            'type': 'receive',
            "data": {
                "method": method,
                "list": DTO.getDataCodeList()
            }
        }
        print(f"SendWebSocketMessageTask: {param}")
        async_to_sync(channel_layer.group_send)(GeneratorCode, param)

    @staticmethod
    def ToCloseQuestionForTask(identificationCode: str):
        """
        1. 发送删除Question QRcode 图片
        2. 删除QRcode图片
        3. 删除Redis
        :param identificationCode:
        :return:
        """
        print("运行")
        Generator.ToCloseForTask(identificationCode)

        # 发送删除QRCode
        param = {
            "code": identificationCode,
            "action": ActionEnum.close.value
        }
        GeneratorCode = Generator.Get()
        data = QuestionAndAnswerDTO(json.dumps(param))
        data.SplitCloseData(identificationCode)
        QrcodeMaker.make(data.getDataList(), data.getDataCodeList())
        Generator.SendWebSocketMessageTask(GeneratorCode, GeneratorsWebSocketMethodEnum.add.value, data)

        time.sleep(3)

        redis_conn = get_redis_connection()
        redis_conn.delete("A" + identificationCode[1:])
        Generator.SendWebSocketMessageTask(GeneratorCode, GeneratorsWebSocketMethodEnum.delete.value, data)

    @staticmethod
    async def ToCloseQuestion(identificationCode: str):
        """
        1. 发送删除Question QRcode 图片
        2. 删除QRcode图片
        3. 删除Redis
        :param identificationCode:
        :return:
        """
        await Generator.ToClose(identificationCode)

        # 发送删除QRCode
        param = {
            "code": identificationCode,
            "action": ActionEnum.close.value
        }
        GeneratorCode = Generator.Get()
        data = QuestionAndAnswerDTO(json.dumps(param))
        data.SplitCloseData(identificationCode)
        QrcodeMaker.make(data.getDataList(), data.getDataCodeList())
        await Generator.SendWebSocketMessage(GeneratorCode, GeneratorsWebSocketMethodEnum.add.value, data)

    @staticmethod
    async def ToCloseAnswer(identificationCode: str):
        identificationCode = identificationCode.replace('C', 'A')
        await Generator.ToClose(identificationCode)

    @staticmethod
    def SetAnswer(result: dict):
        identificationCode: str = result['code']
        identificationCode = identificationCode.replace('A', 'Q')
        question: QuestionAndAnswerEvent = Generator.__EventList[identificationCode]
        question.setData(result['data'])
        question.up()

    @staticmethod
    async def waitAnswer(identificationCode: str):
        question: QuestionAndAnswerEvent = Generator.__EventList[identificationCode]
        await question.wait()

    @staticmethod
    async def Run(data: dict, isQuestion: bool = True, code: str = None):
        GeneratorCode = Generator.Get()

        data = QuestionAndAnswerDTO(json.dumps(data))
        if isQuestion:
            identificationCode = data.SplitQuestionData()
        else:
            identificationCode = data.SplitAnswerData(code)

        event: QuestionAndAnswerEvent = QuestionAndAnswerEvent(identificationCode, GeneratorCode)
        event.SetDTO(data)

        Generator.__EventList[identificationCode] = event
        QrcodeMaker.make(data.getDataList(), data.getDataCodeList())

        await Generator.SendWebSocketMessage(GeneratorCode, GeneratorsWebSocketMethodEnum.add.value, data)
        return identificationCode

    @staticmethod
    async def SendWebSocketMessage(GeneratorCode: str, method: str, DTO: QuestionAndAnswerDTO):
        channel_layer = get_channel_layer()
        param = {
            'type': 'receive',
            "data": {
                "method": method,
                "list": DTO.getDataCodeList()
            }
        }
        print(param)
        await channel_layer.group_send(GeneratorCode, param)

    @staticmethod
    def GetNoGeneratorError():
        raise NoGeneratorError()

    @staticmethod
    def Init():
        Generator.Get = Generator.GetNoGeneratorError

    @staticmethod
    def GetGenerator() -> str:
        GeneratorCode = Generator.__Generators[Generator.__NextGenerator]
        Generator.__NextGenerator += 1
        if Generator.__NextGenerator == Generator.__NowGenerator:
            Generator.__NextGenerator = 0
        return GeneratorCode

    @staticmethod
    def Get() -> str:
        pass

    @staticmethod
    def Add(code):
        Generator.__Generators.append(code)
        Generator.__NowGenerator += 1
        Generator.Get = Generator.GetGenerator

    @staticmethod
    def remove(code):
        Generator.__Generators.remove(code)
        Generator.__NowGenerator -= 1
        if Generator.__NowGenerator == 0:
            Generator.Get = Generator.GetNoGeneratorError

    @staticmethod
    def GetNewGeneratorCode() -> str:
        Generator.__GeneratorCode += 1
        Code = f'Generator_{Generator.__GeneratorCode}'
        Generator.Add(Code)

        return Code
