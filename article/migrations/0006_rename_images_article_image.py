# Generated by Django 5.1.1 on 2024-10-14 14:18

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("article", "0005_rename_image_article_images"),
    ]

    operations = [
        migrations.RenameField(
            model_name="article",
            old_name="images",
            new_name="image",
        ),
    ]
