from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import transaction


class Account(AbstractUser):
    email = models.EmailField(verbose_name="email",
                              max_length=255, unique=True)
    models.EmailField(verbose_name="email",
                      max_length=255, unique=True)
    name = models.CharField(verbose_name="name", max_length=255)
    is_manager = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'name']


class Manager(models.Model):
    account = models.OneToOneField(
        Account, on_delete=models.CASCADE, primary_key=True)

    @transaction.atomic
    def save(self, *args, **kwargs):
        super(Manager, self).save(*args, **kwargs)
        self.account.is_manager = True
        self.account.save()

    def __str__(self):
        return self.account.username


class Plant(models.Model):
    name = models.CharField(max_length=500)
    description = models.TextField(max_length=2000)
    price = models.FloatField()
    manager = models.ForeignKey("Manager", on_delete=models.CASCADE)


class PlantImage(models.Model):
    image = models.ImageField()
    plant = models.ForeignKey('Plant', on_delete=models.CASCADE)


class UserCartPlant(models.Model):
    account = models.ForeignKey('Account', on_delete=models.CASCADE)
    plant = models.ForeignKey('Plant', on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=1)


class Order(models.Model):
    plant = models.ForeignKey('Plant', on_delete=models.CASCADE)
    account = models.ForeignKey('Account', on_delete=models.CASCADE)
    manager = models.ForeignKey("Manager", on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
