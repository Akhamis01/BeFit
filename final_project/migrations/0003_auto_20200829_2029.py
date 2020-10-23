# Generated by Django 3.1 on 2020-08-29 16:29

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('final_project', '0002_user_pic'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='height',
            field=models.IntegerField(default=100, validators=[django.core.validators.MaxValueValidator(250), django.core.validators.MinValueValidator(120)]),
        ),
        migrations.AddField(
            model_name='user',
            name='weight',
            field=models.IntegerField(default=30, validators=[django.core.validators.MaxValueValidator(400), django.core.validators.MinValueValidator(30)]),
        ),
    ]