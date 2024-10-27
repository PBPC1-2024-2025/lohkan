# Generated by Django 5.1 on 2024-10-25 08:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('explore', '0005_alter_food_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='food',
            name='type',
            field=models.CharField(choices=[('MC', 'Main Course'), ('DS', 'Dessert'), ('DR', 'Drinks'), ('SN', 'Snacks')], default='MC', max_length=2),
        ),
    ]
