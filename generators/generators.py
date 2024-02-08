import json

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from Tools import QrcodeMaker
from generators.Exceptions.NoGeneratorError import NoGeneratorError
from generators.QuestionDTO import QuestionDTO


class Generator(object):
    __Generators = []
    __NextGenerator = 0
    __GeneratorCode = 0

    __NowGenerator = 0

    def __init__(self):
        pass

    @staticmethod
    def Run(data: str):
        code = Generator.Get()
        channel_layer = get_channel_layer()

        Q = QuestionDTO(json.dumps(data))
        Q.SplitData()

        QrcodeMaker.make(Q.getDataList(), Q.getDataCodeList())

        param = {
            'type': 'receive',
            "data": {
                "method": "add",
                "list": Q.getDataCodeList()
            }
        }

        async_to_sync(channel_layer.group_send)(code, param)

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
