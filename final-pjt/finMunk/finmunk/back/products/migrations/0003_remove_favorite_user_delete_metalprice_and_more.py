# Generated by Django 4.2.14 on 2025-05-24 02:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0002_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="favorite",
            name="user",
        ),
        migrations.DeleteModel(
            name="MetalPrice",
        ),
        migrations.DeleteModel(
            name="Favorite",
        ),
    ]
