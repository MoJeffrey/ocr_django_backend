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

    @staticmethod
    def make(dataList: list, fileNameList: list, savePath: str = QRCODE_SAVE_PATH) -> list:
        data_list = QrcodeMaker.__ArrayList()
        fileName_list = QrcodeMaker.__ArrayList()

        for i in range(len(dataList)):
            data_list.add(dataList[i])
            fileName_list.add(fileNameList[i])

        param = (
            data_list,
            QrcodeMaker.__QRCode_High,
            QrcodeMaker.__QRCode_Width,
            savePath,
            fileName_list,
            QrcodeMaker.__COLOR_LIST
        )

        QrcodeMaker.__Maker.generateQRCodesWithBackgroundColor(*param)
        return fileNameList

    @staticmethod
    def remove(fileNameList: list, savePath: str = QRCODE_SAVE_PATH):
        for name in fileNameList:
            path = f'{savePath}{name}.jpg'
            try:
                os.remove(path)
            except FileNotFoundError:
                continue
