# Generated by Django 4.0.2 on 2023-01-21 14:54

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hatim', '0006_alter_hatim_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hatim',
            name='created_at',
            field=models.DateField(default=datetime.date.today),
        ),
    ]