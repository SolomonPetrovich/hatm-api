# Generated by Django 4.0.2 on 2023-01-21 11:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hatim', '0003_rename_creator_id_hatim_user_idj'),
    ]

    operations = [
        migrations.RenameField(
            model_name='hatim',
            old_name='user_idj',
            new_name='creator_id',
        ),
    ]
