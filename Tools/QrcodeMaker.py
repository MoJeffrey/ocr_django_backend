import os

import jpype

from ocr_django.settings import QRCODE_SAVE_PATH, QRCODE_COLOR_LIST


class QrcodeMaker:
    __javaToolsName: str = 'qrCodeIdentify.jar'
    __javaToolPath: str = None
    __ArrayList = None
    __Maker = None

    __QRCode_High = 400
    __QRCode_Width = 400
    __COLOR_LIST = None
    __COLOR_INDEX = None
    __COLOR_LENGTH = None

    @staticmethod
    def Init(javaToolPath: str = None):
        QrcodeMaker.__javaToolPath = f"{os.getcwd()}/javaTools/" if javaToolPath is None else javaToolPath
        path = QrcodeMaker.__javaToolPath + QrcodeMaker.__javaToolsName
        jpype.startJVM(jpype.getDefaultJVMPath(), "-ea", f"-Djava.class.path={path}")
        QrcodeMaker.__ArrayList = jpype.JClass("java.util.ArrayList")
        QrcodeMaker.__Maker = jpype.JClass("QRCodeUtil")()
        QrcodeMaker.__Integer = jpype.JClass("java.lang.Integer")
        if not os.path.exists(QRCODE_SAVE_PATH):
            os.makedirs(QRCODE_SAVE_PATH)

        QrcodeMaker.__COLOR_LIST = QrcodeMaker.__ArrayList()
        for i in QRCODE_COLOR_LIST:
            QrcodeMaker.__COLOR_LIST.add(i)

        QrcodeMaker.__COLOR_LENGTH = len(QrcodeMaker.__COLOR_LIST)
        QrcodeMaker.__COLOR_INDEX = 0

    @staticmethod
    def make(dataList: list, fileNameList: list, savePath: str = QRCODE_SAVE_PATH) -> list:
        data_list = QrcodeMaker.__ArrayList()
        fileName_list = QrcodeMaker.__ArrayList()
        color_list = QrcodeMaker.__ArrayList()

        codeList = []
        for i in range(len(dataList)):
            data_list.add(dataList[i])

            fileName = fileNameList[i] + f'_{QrcodeMaker.__COLOR_INDEX + 1}'
            # fileName = fileNameList[i]
            fileName_list.add(fileName)
            codeList.append(fileName)
            color_list.add(QRCODE_COLOR_LIST[QrcodeMaker.__COLOR_INDEX])

            QrcodeMaker.__COLOR_INDEX += 1
            if QrcodeMaker.__COLOR_INDEX == QrcodeMaker.__COLOR_LENGTH:
                QrcodeMaker.__COLOR_INDEX = 0

        param = (
            data_list,
            QrcodeMaker.__QRCode_High,
            QrcodeMaker.__QRCode_Width,
            savePath,
            fileName_list,
            color_list
        )

        QrcodeMaker.__Maker.generateQRCodesWithBackgroundColor(*param)
        return codeList

    @staticmethod
    def remove(fileNameList: list, savePath: str = QRCODE_SAVE_PATH):
        for name in fileNameList:
            path = f'{savePath}{name}.jpg'
            try:
                os.remove(path)
            except FileNotFoundError:
                continue
