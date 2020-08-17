from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('signup/', views.signup, name="signup"),
    path('signup-as-manager/', views.signup_as_manager, name="signup-as-manager"),
    path('create-account/', views.create_account, name="create-account"),
    path('create-manager/', views.create_manager, name="create-manager"),
    path('login/', views.account_login, name="login"),
    path('logout/', views.account_logout, name="logout"),
    path('add-plant/', views.add_plant, name="add-plant"),
    path('add-to-cart/', views.add_to_cart, name="add-to-cart"),
    path('cart/', views.cart, name="cart"),
    path('place-order/', views.place_order, name="place-order"),
    path('received-orders/', views.received_orders, name="received-orders"),
    path('dispatch-orders/', views.dispatch_orders, name="dispatch-orders"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
