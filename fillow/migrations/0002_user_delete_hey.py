# Generated by Django 4.2.7 on 2023-12-19 03:06

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("fillow", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("user_id", models.CharField(max_length=20)),
                ("user_pw", models.CharField(max_length=30)),
                ("user_dep", models.CharField(max_length=10)),
                ("user_email", models.EmailField(max_length=254)),
            ],
        ),
        migrations.DeleteModel(
            name="hey",
        ),
    ]
