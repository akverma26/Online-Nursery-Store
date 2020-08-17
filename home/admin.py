from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Account, Manager, Plant, PlantImage, Order, UserCartPlant

# Register your models here.
admin.site.register(
    [Account, Manager, Plant, PlantImage, UserCartPlant, Order])
