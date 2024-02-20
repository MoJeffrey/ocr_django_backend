import asyncio
import json
import logging

from asgiref.sync import async_to_sync
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
    data = Generator.GetAnswer(identificationCode)

    return JsonResponse(data)


async def test(request):
    await asyncio.sleep(1)
    return JsonResponse({'message': 'Async view completed'})
