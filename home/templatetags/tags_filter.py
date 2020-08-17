from django import template
from django.template.defaultfilters import stringfilter

from ..models import PlantImage

register = template.Library()


@register.filter
def get_images(plant):
    return PlantImage.objects.filter(plant=plant)
