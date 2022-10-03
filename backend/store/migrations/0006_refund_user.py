# Generated by Django 4.1.1 on 2022-10-03 18:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0005_user_is_anonymous_user_is_authenticated"),
    ]

    operations = [
        migrations.AddField(
            model_name="refund",
            name="user",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
