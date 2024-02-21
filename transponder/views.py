import asyncio
import json

from django_redis import get_redis_connection
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
    # await Generator.ToCloseQuestion(identificationCode)

    return JsonResponse(data)


async def test(request):
    await asyncio.sleep(1)
    redis_conn = get_redis_connection()
    redis_conn.delete('A000000001')
    return JsonResponse({'message': 'hi'})
