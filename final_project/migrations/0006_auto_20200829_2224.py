# Generated by Django 3.1 on 2020-08-29 18:24

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('final_project', '0005_auto_20200829_2115'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='height',
            field=models.IntegerField(default=100, help_text='Value must be in Cm, between 120-250cm', validators=[django.core.validators.MaxValueValidator(250), django.core.validators.MinValueValidator(120)]),
        ),
        migrations.AlterField(
            model_name='user',
            name='weight',
            field=models.IntegerField(default=30, help_text='Value must be in Kg, between 30-400kg', validators=[django.core.validators.MaxValueValidator(400), django.core.validators.MinValueValidator(30)]),
        ),
    ]
