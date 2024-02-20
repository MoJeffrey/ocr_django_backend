"""
URL configuration for ocr_django project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from generators.GeneratorsWebSocket import GeneratorsWebSocket
from recognizer.RecognizerWebSocket import RecognizerWebSocket
from transponder import views as transponder

websocket_urlpatterns = [
    path('ws/generators/', GeneratorsWebSocket.as_asgi()),
    path('ws/recognizer/', RecognizerWebSocket.as_asgi()),
]

urlpatterns = [
    path('question/<path:url>', transponder.APITransponder),
    path('test', transponder.test),
]


