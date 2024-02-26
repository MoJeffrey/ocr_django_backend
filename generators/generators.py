import json
import time

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from Tools import QrcodeMaker
from generators.DTO.QuestionAndAnswerDTO import QuestionAndAnswerDTO
from generators.QuestionAndAnswerEvent import QuestionAndAnswerEvent
from generators.enum.ActionEnum import ActionEnum
from generators.enum.GeneratorsWebSocketMethodEnum import GeneratorsWebSocketMethodEnum
from recognizer.DTO.RecognizerDTO import RecognizerDTO
from recognizer.recognizer import Recognizer


class Generator(object):
    __Generators = []
    __EventList = {}
    __lastGenerator = 0

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
        3. 删除識別程序的數據
        :param identificationCode:
        :return:
        """
        question: QuestionAndAnswerEvent = Generator.__EventList[identificationCode]
        param = (GeneratorsWebSocketMethodEnum.delete.value, question.DTO)
        await Generator.SendMessage(*param)

        QrcodeMaker.remove(question.DTO.getDataCodeList())

        del Generator.__EventList[identificationCode]
        Recognizer.SendDelData(identificationCode)

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
        param = (GeneratorsWebSocketMethodEnum.delete.value, question.DTO)
        Generator.SendWebSocketMessageTask(*param)

        QrcodeMaker.remove(question.DTO.getDataCodeList())

        del Generator.__EventList[identificationCode]

    @staticmethod
    def ToCloseQuestionForTask(identificationCode: str):
        """
        1. 发送删除Question QRcode 图片
        2. 删除QRcode图片
        3. 删除Redis
        :param identificationCode:
        :return:
        """
        Generator.ToCloseForTask(identificationCode)

        # 发送删除QRCode
        param = {
            "code": identificationCode,
            "action": ActionEnum.close.value
        }
        data = QuestionAndAnswerDTO(json.dumps(param))
        CloseCode = data.SplitCloseData(identificationCode)
        QrcodeMaker.make(data.getDataList(), data.getDataCodeList())
        Generator.SendWebSocketMessageTask(GeneratorsWebSocketMethodEnum.add.value, data)

        time.sleep(3)
        Generator.SendWebSocketMessageTask(GeneratorsWebSocketMethodEnum.delete.value, data)
        QrcodeMaker.remove(data.getDataCodeList())
        Recognizer.SendDelData(identificationCode)
        Recognizer.SendDelData(CloseCode)

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
        data = QuestionAndAnswerDTO(json.dumps(param))
        data.SplitCloseData(identificationCode)
        QrcodeMaker.make(data.getDataList(), data.getDataCodeList())
        await Generator.SendMessage(GeneratorsWebSocketMethodEnum.add.value, data)

    @staticmethod
    async def ToCloseAnswer(identificationCode: str):
        identificationCode = identificationCode.replace('C', 'A')
        await Generator.ToClose(identificationCode)

    @staticmethod
    def SetAnswer(DTD: RecognizerDTO):
        identificationCode: str = DTD.code
        identificationCode = identificationCode.replace('A', 'Q')
        question: QuestionAndAnswerEvent = Generator.__EventList[identificationCode]
        question.setData(DTD.data)
        question.up()

    @staticmethod
    async def waitAnswer(identificationCode: str):
        question: QuestionAndAnswerEvent = Generator.__EventList[identificationCode]
        await question.wait()

    @staticmethod
    async def Run(data: dict, isQuestion: bool = True, code: str = None):
        data = QuestionAndAnswerDTO(json.dumps(data))
        if isQuestion:
            identificationCode = data.SplitQuestionData()
        else:
            identificationCode = data.SplitAnswerData(code)

        event: QuestionAndAnswerEvent = QuestionAndAnswerEvent(identificationCode)
        event.SetDTO(data)

        Generator.__EventList[identificationCode] = event
        QrcodeMaker.make(data.getDataList(), data.getDataCodeList())

        await Generator.SendMessage(GeneratorsWebSocketMethodEnum.add.value, data)
        return identificationCode

    @staticmethod
    async def SendMessage(method: str, DTO: QuestionAndAnswerDTO):
        channel_layer = get_channel_layer()
        allGenerator = len(Generator.__Generators)
        param = {
            'type': 'receive',
            "data": {
                "method": method,
                "list": DTO.getDataCodeList(),
                "lastGenerator": Generator.__lastGenerator,
                "allGenerator": allGenerator
            }
        }
        await channel_layer.group_send('Generator', param)
        Num = (len(DTO.getDataCodeList()) + Generator.__lastGenerator)
        Generator.__lastGenerator = Num % allGenerator

    @staticmethod
    def SendWebSocketMessageTask(method: str, DTO: QuestionAndAnswerDTO):
        channel_layer = get_channel_layer()
        allGenerator = len(Generator.__Generators)
        param = {
            'type': 'receive',
            "data": {
                "method": method,
                "list": DTO.getDataCodeList(),
                "lastGenerator": Generator.__lastGenerator,
                "allGenerator": allGenerator
            }
        }
        async_to_sync(channel_layer.group_send)('Generator', param)
        Num = (len(DTO.getDataCodeList()) + Generator.__lastGenerator)
        Generator.__lastGenerator = Num % allGenerator

    @staticmethod
    def Add(code):
        Generator.__Generators.append(code)

    @staticmethod
    def remove(code):
        Generator.__Generators.remove(code)

    @staticmethod
    def GetNewGeneratorCode() -> str:
        code = 1
        while True:
            if str(code) in Generator.__Generators:
                code += 1
                continue
            break

        code = str(code)
        Generator.Add(code)

        return code
