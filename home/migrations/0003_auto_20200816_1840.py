# Generated by Django 3.1 on 2020-08-16 18:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_auto_20200816_1712'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plant',
            name='manager',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.manager'),
        ),
    ]
