# https://stackoverflow.com/questions/34006994/how-to-upload-multiple-images-to-a-blog-post-in-django
# https://docs.djangoproject.com/en/3.1/topics/forms/formsets/#using-a-formset-in-views-and-templates

from django.shortcuts import render, redirect
from django.http import JsonResponse

from django.db import transaction
from django.forms import modelformset_factory
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from rest_framework.response import Response
from rest_framework.decorators import api_view

from .forms import CreateUserForm, AddPlantForm, AddPlantImageForm, LoginForm
from .models import Account, Manager, Plant, PlantImage, UserCartPlant, Order


def verify_request(request):
    is_manager = False
    logged_in = False
    user = None
    if request.user is not None:
        user = request.user
        try:
            is_manager = Account.objects.get(email=request.user).is_manager
            logged_in = True
        except:
            logged_in = False
            pass

    return {
        "logged_in": logged_in,
        "user": user,
        "is_manager": is_manager,
    }


def home(request):
    plants = Plant.objects.all()
    context = verify_request(request)
    context["plants"] = plants
    return render(request, 'index.html', context)


def signup(request):
    context = verify_request(request)
    if context["logged_in"]:
        return redirect('home')
    form = CreateUserForm()
    context["form"] = form
    return render(request, 'signup.html', context)


def signup_as_manager(request):
    context = verify_request(request)
    if context["logged_in"]:
        return redirect('home')
    form = CreateUserForm()
    context["form"] = form
    return render(request, 'signup-as-manager.html', context)


def create_account(request):
    context = verify_request(request)
    if context["logged_in"]:
        return redirect('home')
    form = CreateUserForm(request.POST)
    form.save()
    return redirect('login')


@transaction.atomic
def create_manager(request):
    context = verify_request(request)
    if context["logged_in"]:
        return redirect('home')
    form = CreateUserForm(request.POST)
    Manager(account=Account.objects.get(email=form.save())).save()
    # print(form.save(), form.cleaned_data.get('email'))
    return redirect('login')


def account_login(request):
    context = verify_request(request)
    if context["logged_in"]:
        return redirect('home')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        print(username, password)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
    form = LoginForm()
    context["form"] = form
    return render(request, 'login.html', context)


@transaction.atomic
def add_plant_to_db(request, ImageFormset):
    plant_form = AddPlantForm(request.POST)
    image_formset = ImageFormset(request.POST, request.FILES)
    if plant_form.is_valid() and image_formset.is_valid():
        plant = Plant(
            name=request.POST['name'],
            description=request.POST['description'],
            price=request.POST['price'],
            manager=Manager(account=Account.objects.get(email=request.user))
        )
        plant.save()
        for form in image_formset.cleaned_data:
            if form and form['image']:
                PlantImage(image=form['image'], plant=plant).save()
    else:
        raise ValueError("Validation Error!")


@login_required(login_url='/login/')
def add_plant(request):
    context = verify_request(request)
    form = AddPlantForm()
    ImageFormset = modelformset_factory(
        PlantImage, form=AddPlantImageForm, extra=4, exclude=('plant',))

    if request.method == "POST":
        add_plant_to_db(request, ImageFormset)
        return redirect('home')

    image_formset = ImageFormset(queryset=PlantImage.objects.none())
    context["form"] = form
    context["image_formset"] = image_formset

    return render(request, 'add-plant.html', {"form": form, "image_formset": image_formset})


def account_logout(request):
    logout(request)
    return redirect('home')


def add_to_cart(request):
    plant_id = request.GET.get('plantId')
    account = Account.objects.get(
        email=request.user)
    plant = Plant.objects.get(id=plant_id)
    try:
        user_cart_plant = UserCartPlant.objects.get(
            account=account, plant=plant)
        user_cart_plant.quantity = user_cart_plant.quantity+1
        user_cart_plant.save()
    except:
        UserCartPlant(account=account, plant=plant).save()
    return JsonResponse({'success': True})


@login_required(login_url='/login/')
def cart(request):
    context = verify_request(request)
    user_cart_plant = UserCartPlant.objects.filter(
        account=Account.objects.get(email=request.user))
    context["user_cart"] = user_cart_plant
    return render(request, 'cart.html', context)


@login_required(login_url='/login/')
def place_order(request):
    context = verify_request(request)
    cart = UserCartPlant.objects.filter(
        account=Account.objects.get(email=request.user))
    for plant in cart:
        Order(plant=plant.plant, account=plant.account,
              quantity=plant.quantity, manager=plant.plant.manager).save()
        plant.delete()
    return redirect('cart')


@login_required(login_url='/login/')
def received_orders(request):
    context = verify_request(request)
    orders = Order.objects.filter(
        manager=Manager.objects.get(
            account=Account.objects.get(email=request.user)))
    context["orders"] = orders
    return render(request, 'received-orders.html', context)


@login_required(login_url='/login/')
def dispatch_orders(request):
    context = verify_request(request)
    orders = Order.objects.filter(
        manager=Manager.objects.get(
            account=Account.objects.get(email=request.user)))
    for order in orders:
        order.delete()
    return redirect('received-orders')
