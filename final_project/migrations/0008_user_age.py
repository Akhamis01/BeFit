# Generated by Django 3.1 on 2020-09-01 16:27

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('final_project', '0007_auto_20200829_2247'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='age',
            field=models.IntegerField(default=18, help_text='Must be between 13-80 years old', validators=[django.core.validators.MaxValueValidator(80), django.core.validators.MinValueValidator(13)]),
        ),
    ]
