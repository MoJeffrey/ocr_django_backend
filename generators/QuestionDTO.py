from ocr_django.settings import QRCODE_MAX_Length


class QuestionDTO:
    __data: str = None
    __dataList: list = None
    __dataCodeList: list = None
    QuestionCode: int = 0
    ActionCode: int = None
    MAX_LENGTH: int = QRCODE_MAX_Length

    def __init__(self, data: str):
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

    def SplitData(self):
        self.__dataList = QuestionDTO.split_string_into_chunks(self.__data, QuestionDTO.MAX_LENGTH)
        self.__dataCodeList = []

        QuestionDTO.QuestionCode += 1
        for num in range(len(self.__dataList)):
            code = "Q" + "%09d" % QuestionDTO.QuestionCode + f"_{num + 1}_{len(self.__dataList)}"
            self.__dataCodeList.append(code)
            self.__dataList[num] = f"[{code}]" + self.__dataList[num]

    def getDataList(self) -> list:
        return self.__dataList

    def getDataCodeList(self) -> list:
        return self.__dataCodeList
