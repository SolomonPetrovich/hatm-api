# Generated by Django 4.0.2 on 2023-06-02 13:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('hatm', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='hatm',
            name='members',
            field=models.ManyToManyField(related_name='members', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='JoinRequest',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('rejected', 'Rejected'), ('approved', 'Approved'), ('pending', 'Pending')], default='pending', max_length=50)),
                ('hatm', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='join_requests', to='hatm.hatm')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
