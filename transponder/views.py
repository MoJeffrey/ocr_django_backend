import json
import threading
import time

from django.http import JsonResponse

from generators.enum.ActionEnum import ActionEnum
from generators.generators import Generator


async def APITransponder(request, url):
    param = {
        "url": url,
        "headers": {'AUTHORIZATION': request.META.get("HTTP_AUTHORIZATION")},
        "method": request.method,
        "action": ActionEnum.transponder.value
    }
    if request.method == "GET":
        param['params'] = request.GET.dict()
    elif request.method == "POST":
        param["data"] = json.loads(request.body) if request.body else {}

    identificationCode = await Generator.Run(param)
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
