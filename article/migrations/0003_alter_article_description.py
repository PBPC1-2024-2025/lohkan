# Generated by Django 5.1.1 on 2024-10-11 04:32

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("article", "0002_alter_article_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="article",
            name="description",
            field=models.TextField(),
        ),
    ]
