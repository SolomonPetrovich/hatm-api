# Generated by Django 4.0.2 on 2023-01-20 18:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('hatim', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='juz',
            name='user_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='juz_set', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='hatim',
            name='creator_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]