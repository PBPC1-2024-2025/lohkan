# Generated by Django 5.1.1 on 2024-10-11 04:49

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("article", "0003_alter_article_description"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="article",
            name="user",
        ),
    ]
