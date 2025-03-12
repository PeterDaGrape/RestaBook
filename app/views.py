from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    respnse = render(request, 'restabook/index.html')
    return respnse