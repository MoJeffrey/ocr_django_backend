import json

from ocr_django.settings import QRCODE_MAX_Length
from recognizer.DTO.RecognizerDTO import RecognizerDTO


class QuestionAndAnswerDTO:
    __data: RecognizerDTO = None
    __dataList: list = None
    __dataCodeList: list = None
    QuestionCode: int = 0
    ActionCode: int = None
    MAX_LENGTH: int = QRCODE_MAX_Length

    def __init__(self, data: RecognizerDTO):
        self.__data = data

    @staticmethod
    def split_string_into_chunks(input_string, chunk_size):
        """
        数据拆分
        :param input_string:
        :param chunk_size:
        :return:
        """
        return [input_string[i:i + chunk_size] for i in range(0, len(input_string), chunk_size)]

    def GetData(self) -> RecognizerDTO:
        return self.__data

    def SplitData(self, code, identification):
        code = identification + "%09d" % code
        self.__data.code = code

        data = json.dumps(self.__data.GetData())
        LENGTH = QuestionAndAnswerDTO.MAX_LENGTH

        self.__dataList = QuestionAndAnswerDTO.split_string_into_chunks(data, LENGTH)
        self.__dataCodeList = []
        for num in range(len(self.__dataList)):
            TheCode = code + f"_{num + 1}_{len(self.__dataList)}"
            self.__dataCodeList.append(TheCode)
            self.__dataList[num] = f"[{TheCode}]" + self.__dataList[num]

        return code

    def SplitCloseData(self, code: str):
        code = int(code[1:])
        return self.SplitData(code, 'C')

    def SplitQuestionData(self):
        QuestionAndAnswerDTO.QuestionCode += 1
        return self.SplitData(QuestionAndAnswerDTO.QuestionCode, 'Q')

    def SplitAnswerData(self, code):
        code = int(code[1:])
        return self.SplitData(code, 'A')

    def getDataList(self) -> list:
        return self.__dataList

    def getDataCodeList(self) -> list:
        return self.__dataCodeList

    def setDataCodeList(self, codeList: list):
        self.__dataCodeList = codeList
