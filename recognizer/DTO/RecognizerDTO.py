import json


class RecognizerDTO:
    action: str = None
    data: dict = None
    code: str = None

    def __init__(self, StringObj: str = None, Object: dict = None):
        if StringObj is not None:
            data = json.loads(StringObj)
            self.__dict__ = data.copy()

        if Object is not None:
            self.__dict__ = Object.copy()

    def GetData(self) -> dict:
        return {
            'action': self.action,
            'data': self.data,
            'code': self.code
        }
