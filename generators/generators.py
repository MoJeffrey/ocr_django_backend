import json

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from Tools import QrcodeMaker
from generators.Exceptions.NoGeneratorError import NoGeneratorError
from generators.DTO.QuestionAndAnswerDTO import QuestionAndAnswerDTO
from generators.QuestionEvent import QuestionEvent


class Generator(object):
    __Generators = []
    __QuestionList = {}
    __NextGenerator = 0
    __GeneratorCode = 0

    __NowGenerator = 0

    def __init__(self):
        pass

    @staticmethod
    def GetAnswer(identificationCode: str):
        question = Generator.__QuestionList[identificationCode]
        data = question.getData()
        del Generator.__QuestionList[identificationCode]
        return data

    @staticmethod
    def SetAnswer(result: dict):
        identificationCode: str = result['code']
        identificationCode = identificationCode.replace('A', 'Q')
        question: QuestionEvent = Generator.__QuestionList[identificationCode]
        question.setData(result['data'])
        question.up()

    @staticmethod
    async def waitAnswer(identificationCode: str):
        question: QuestionEvent = Generator.__QuestionList[identificationCode]
        await question.wait()

    @staticmethod
    async def Run(data: dict, isQuestion: bool = True, code: str = None):
        GeneratorCode = Generator.Get()
        channel_layer = get_channel_layer()

        data = QuestionAndAnswerDTO(json.dumps(data))
        if isQuestion:
            identificationCode = data.SplitQuestionData()
            Generator.__QuestionList[identificationCode] = QuestionEvent(identificationCode)
        else:
            identificationCode = data.SplitAnswerData(code)

        QrcodeMaker.make(data.getDataList(), data.getDataCodeList())

        param = {
            'type': 'receive',
            "data": {
                "method": "add",
                "list": data.getDataCodeList()
            }
        }

        await channel_layer.group_send(GeneratorCode, param)
        # async_to_sync()()

        return identificationCode

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
