from .AutomationLogic import automatedTestCases
from django.shortcuts import render
from django.shortcuts import render
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from django.core import  serializers
from django.conf import settings
import json
from selenium import webdriver
from bs4 import BeautifulSoup
import time
from selenium.webdriver.support import expected_conditions as EC

# Create your views here.
from selenium.webdriver.support.wait import WebDriverWait


def homepage(request):
    return render(request, 'index.html')


@api_view(["POST"])
def AutomatedSanityAPI(dataArray):
    try:
        response = json.loads(dataArray.body)
        automatedTestCases(response)
        return JsonResponse(response, safe=False)
    except ValueError as e:
        return Response(e.args[0], status.HTTP_400_BAD_REQUEST)
