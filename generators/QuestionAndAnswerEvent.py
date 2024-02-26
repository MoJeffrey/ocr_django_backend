import asyncio

from generators.DTO.QuestionAndAnswerDTO import QuestionAndAnswerDTO


class QuestionAndAnswerEvent:
    identificationCode: str = None
    event = None
    data = None
    DTO: QuestionAndAnswerDTO = None

    def __init__(self, identificationCode):
        self.identificationCode = identificationCode
        self.event = asyncio.Event()

    def SetDTO(self, DTO):
        self.DTO = DTO

    def GetDTO(self) -> QuestionAndAnswerDTO:
        return self.DTO

    async def wait(self):
        """
        等待
        :return:
        """
        await self.event.wait()

    def up(self):
        """
        启动
        :return:
        """
        self.event.set()

    def getData(self):
        return self.data

    def setData(self, data):
        self.data = data
