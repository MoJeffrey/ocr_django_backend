import json
import threading
import time

from django.http import JsonResponse

from generators.enum.ActionEnum import ActionEnum
from generators.generators import Generator
from recognizer.DTO.RecognizerDTO import RecognizerDTO
from transponder.Transponder import Transponder


async def APITransponder(request, url):
    transponder = Transponder()
    transponder.url = url
    transponder.headers = {'AUTHORIZATION': request.META.get("HTTP_AUTHORIZATION")}
    transponder.method = request.method

    if request.method == "GET":
        transponder.params = request.GET.dict()
    elif request.method == "POST":
        transponder.data = json.loads(request.body) if request.body else {}

    DTO = RecognizerDTO()
    DTO.action = ActionEnum.transponder.value
    DTO.data = transponder.GetTransponderData()

    identificationCode = await Generator.Run(DTO)
    await Generator.waitAnswer(identificationCode)
    data = await Generator.GetAnswer(identificationCode)

    background_thread = threading.Thread(target=Generator.ToCloseQuestionForTask, args=(identificationCode, ))
    background_thread.start()

    return JsonResponse(data)


def long_running_task():
    time.sleep(2)
    print("Long running task completed")


def test(request):
    background_thread = threading.Thread(target=long_running_task)
    background_thread.start()
    print("运行完成")
    return JsonResponse({'message': 'hi'})
