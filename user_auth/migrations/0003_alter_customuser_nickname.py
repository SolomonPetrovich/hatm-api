# Generated by Django 4.0.2 on 2023-01-30 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_auth', '0002_alter_customuser_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='nickname',
            field=models.CharField(default=None, max_length=150),
        ),
    ]