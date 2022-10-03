# Generated by Django 4.1.1 on 2022-09-16 18:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0001_initial"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Admin",
        ),
        migrations.AlterField(
            model_name="user",
            name="role",
            field=models.CharField(
                choices=[("STAFF", "Staff"), ("CUSTOMER", "Customer")],
                default="CUSTOMER",
                max_length=50,
                verbose_name="Roles",
            ),
        ),
    ]