# Generated by Django 4.2 on 2025-01-20 02:21

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("post", "0002_comment"),
    ]

    operations = [
        migrations.AddField(
            model_name="post",
            name="like",
            field=models.ManyToManyField(
                blank=True, related_name="likes", to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
