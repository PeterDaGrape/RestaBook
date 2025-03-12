from django.shortcuts import render
from django.http import HttpResponse

from app.models import Restaurant


def index(request):
    restaurant_list = Restaurant.objects.all()[:5]
    context_dict = {}
    context_dict['restaurants'] = restaurant_list
    response = render(request, 'restabook/index.html', context=context_dict)
    return response
