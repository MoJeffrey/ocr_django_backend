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
        1. 向前端发送删除 答案二维码
        2. 删除答案二维码图片
        3. 删除答案二维码列表
        4. 发送识别端删除问题码数据
        5. 删除问题码数据
        :param identificationCode:
        :return:
        """
        identificationCode = identificationCode.replace('C', 'A')
        question: QuestionAndAnswerEvent = Generator.__EventList[identificationCode]
        param = (GeneratorsWebSocketMethodEnum.delete.value, question.DTO)
        await Generator.SendMessage(*param)

        QrcodeMaker.remove(question.DTO.getDataCodeList())

        del Generator.__EventList[identificationCode]

        identificationCode = identificationCode.replace('A', 'Q')
        Recognizer.SendDelData(identificationCode)

        Recognizer.DeleteResult(identificationCode)

    @staticmethod
    def ToCloseForTask(identificationCode: str):
        """
        1. 发送给前端删除QR 图片显示
        2. 删除创建的QR 图片文件
        3. 列表中删除该问题
        :param identificationCode:
        :return:
        """
        question: QuestionAndAnswerEvent = Generator.__EventList[identificationCode]
        param = (GeneratorsWebSocketMethodEnum.delete.value, question.DTO)
        Generator.SendWebSocketMessageTask(*param)

        QrcodeMaker.remove(question.DTO.getDataCodeList())

        del Generator.__EventList[identificationCode]

    @staticmethod
    def SendCloseQRCode(identificationCode: str) -> QuestionAndAnswerDTO:
        """
        传入识别码

        向前端send 关闭该问题的二维码

        告诉内容服务器停止显示答案二维码
        :param identificationCode:
        :return:
        """
        DTO = RecognizerDTO()
        DTO.action = ActionEnum.close.value
        DTO.code = identificationCode

        data = QuestionAndAnswerDTO(DTO)
        data.SplitCloseData(identificationCode)
        codeList = QrcodeMaker.make(data.getDataList(), data.getDataCodeList())
        data.setDataCodeList(codeList)

        Generator.SendWebSocketMessageTask(GeneratorsWebSocketMethodEnum.add.value, data)
        return data

    @staticmethod
    def ToCloseQuestionForTask(identificationCode: str):
        """
        1. 删除东西
        2. 发送删除问题二维码
        3. 等待收到内网服务器收到删除指令
        :param identificationCode:
        :return:
        """
        Generator.ToCloseForTask(identificationCode)

        DTO = Generator.SendCloseQRCode(identificationCode)

        # time.sleep(3)
        # Generator.SendWebSocketMessageTask(GeneratorsWebSocketMethodEnum.delete.value, DTO)
        # QrcodeMaker.remove(DTO.getDataCodeList())
        # Recognizer.SendDelData(identificationCode)
        # Recognizer.SendDelData(DTO.GetData().code)

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
        DTO = RecognizerDTO()
        DTO.action = ActionEnum.close.value
        DTO.code = identificationCode

        data = QuestionAndAnswerDTO(DTO)
        data.SplitCloseData(identificationCode)

        codeList = QrcodeMaker.make(data.getDataList(), data.getDataCodeList())
        data.setDataCodeList(codeList)

        await Generator.SendMessage(GeneratorsWebSocketMethodEnum.add.value, data)

    @staticmethod
    async def ToCloseAnswer(identificationCode: str):
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
    async def Run(data: RecognizerDTO, isQuestion: bool = True, code: str = None):
        data = QuestionAndAnswerDTO(data)
        if isQuestion:
            identificationCode = data.SplitQuestionData()
        else:
            identificationCode = data.SplitAnswerData(code)

        event: QuestionAndAnswerEvent = QuestionAndAnswerEvent(identificationCode)
        event.SetDTO(data)

        Generator.__EventList[identificationCode] = event
        codeList = QrcodeMaker.make(data.getDataList(), data.getDataCodeList())
        data.setDataCodeList(codeList)

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
