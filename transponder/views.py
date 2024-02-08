import json

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from generators.generators import Generator


@method_decorator(csrf_exempt)
def APITransponder(request, url):
    param = {
        "url": request.path,
        "headers": [],
        "method": request.method,
        "data": json.loads(request.body),
        "action": "transponder"
    }

    Generator.Run(param)

    return JsonResponse(param)
