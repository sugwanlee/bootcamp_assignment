# Generated by Django 4.2 on 2025-01-13 22:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0005_alter_customuser_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customuser",
            name="image",
            field=models.ImageField(
                default="default_images/default.png", upload_to="image/"
            ),
        ),
    ]
