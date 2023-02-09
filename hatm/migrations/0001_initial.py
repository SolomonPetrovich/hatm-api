# Generated by Django 4.0.2 on 2023-02-09 11:48

import datetime
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Hatm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('description', models.TextField()),
                ('is_public', models.BooleanField()),
                ('is_completed', models.BooleanField(default=False)),
                ('is_published', models.BooleanField(default=False)),
                ('created_at', models.DateField(default=datetime.date.today)),
                ('deadline', models.DateField()),
            ],
            options={
                'verbose_name': 'Hatm',
                'verbose_name_plural': 'Hatms',
            },
        ),
        migrations.CreateModel(
            name='Juz',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('juz_number', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(31)])),
                ('type', models.CharField(choices=[('juz', 'Juz'), ('dua', 'Dua')], max_length=50)),
                ('status', models.CharField(choices=[('free', 'Free'), ('in Progress', 'In Progress'), ('completed', 'Completed')], default='free', max_length=20)),
                ('hatm_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='juz', to='hatm.hatm')),
            ],
            options={
                'verbose_name': 'Juz',
                'verbose_name_plural': 'Juzs',
            },
        ),
    ]
