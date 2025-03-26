from django import template
from app.models import Restaurant

register = template.Library()

@register.inclusion_tag('app/restaurant_list.html')
def get_restaurant_list():
    return {'restaurants': Restaurant.objects.all()}
