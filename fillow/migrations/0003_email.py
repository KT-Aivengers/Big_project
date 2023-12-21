# Generated by Django 4.2 on 2023-12-21 01:51

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("fillow", "0002_document_alter_user_user_phone"),
    ]

    operations = [
        migrations.CreateModel(
            name="Email",
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
                ("email_file_name", models.CharField(max_length=100)),
                ("email_subject", models.CharField(max_length=100)),
                ("email_date", models.CharField(max_length=100)),
                ("email_from", models.CharField(max_length=100)),
                ("email_to", models.CharField(max_length=100)),
                ("email_cc", models.CharField(max_length=100)),
                ("email_text_content", models.CharField(max_length=5000)),
            ],
        ),
    ]
