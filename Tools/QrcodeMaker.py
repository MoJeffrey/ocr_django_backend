import os

import jpype

from ocr_django.settings import QRCODE_SAVE_PATH


class QrcodeMaker:
    __javaToolsName: str = 'qrCodeIdentify.jar'
    __javaToolPath: str = None
    __ArrayList = None
    __Maker = None

    __QRCode_High = 400
    __QRCode_Width = 400

    @staticmethod
    def Init(javaToolPath: str = None):
        QrcodeMaker.__javaToolPath = f"{os.getcwd()}/javaTools/" if javaToolPath is None else javaToolPath
        path = QrcodeMaker.__javaToolPath + QrcodeMaker.__javaToolsName
        jpype.startJVM(jpype.getDefaultJVMPath(), "-ea", f"-Djava.class.path={path}")
        QrcodeMaker.__ArrayList = jpype.JClass("java.util.ArrayList")
        QrcodeMaker.__Maker = jpype.JClass("QRCodeUtil")()

    @staticmethod
    def make(dataList: list, fileNameList: list, savePath: str = QRCODE_SAVE_PATH) -> list:
        data_list = QrcodeMaker.__ArrayList()
        fileName_list = QrcodeMaker.__ArrayList()

        for i in range(len(dataList)):
            data_list.add(dataList[i])
            fileName_list.add(fileNameList[i])

        param = (
            data_list,
            fileName_list,
            savePath,
            QrcodeMaker.__QRCode_High,
            QrcodeMaker.__QRCode_Width
        )
        items = QrcodeMaker.__Maker.generateQRCodeImage(*param)
        return list(items)

    @staticmethod
    def remove(fileNameList: list, savePath: str = QRCODE_SAVE_PATH):
        for name in fileNameList:
            path = f'{savePath}{name}.jpg'
            try:
                os.remove(path)
            except FileNotFoundError:
                continue
