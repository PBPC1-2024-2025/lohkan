# Generated by Django 5.1.2 on 2024-10-25 17:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('explore', '0007_food_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='food',
            name='user',
        ),
    ]
