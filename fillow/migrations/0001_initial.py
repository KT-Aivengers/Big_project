# Generated by Django 4.2 on 2024-01-02 01:55

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AdditionalInform',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('department', models.CharField(max_length=10)),
                ('phone', models.CharField(max_length=16, validators=[django.core.validators.RegexValidator(message='010-****-****의 형태로 입력해주세요.', regex='^01([0|1|6|7|8|9]?)-?([0-9]{3,4})-?([0-9]{4})$')])),
                ('introduce', models.CharField(max_length=500)),
                ('image', models.ImageField(upload_to='profile/')),
                ('company', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uploaded_file', models.FileField(upload_to='documents/')),
            ],
        ),
        migrations.CreateModel(
            name='Qna',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(blank=True, max_length=300)),
                ('answer', models.CharField(blank=True, max_length=300)),
                ('title', models.CharField(blank=True, max_length=50)),
                ('edit_date', models.DateField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='qna', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='EmailComposeTpl',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('texts', models.CharField(blank=True, max_length=1000)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='email_tpl', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='EmailCompose',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email_to', models.CharField(max_length=1000)),
                ('email_cc', models.CharField(blank=True, max_length=1000)),
                ('email_subject', models.CharField(max_length=100)),
                ('email_file', models.FileField(blank=True, upload_to='documents/compose/')),
                ('email_text_content', models.CharField(max_length=1000)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='email_compose', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Email',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email_file_name', models.CharField(max_length=100)),
                ('email_subject', models.CharField(max_length=100)),
                ('email_from', models.CharField(max_length=1000)),
                ('email_to', models.CharField(max_length=1000)),
                ('email_cc', models.CharField(max_length=1000, null=True)),
                ('email_file', models.FileField(null=True, upload_to='uploads/')),
                ('email_text_content', models.CharField(max_length=10000)),
                ('email_date', models.CharField(max_length=100)),
                ('category', models.CharField(max_length=100)),
                ('from_company', models.CharField(max_length=100)),
                ('from_dept', models.CharField(max_length=100)),
                ('from_name', models.CharField(max_length=100)),
                ('reply_req_yn', models.BooleanField(default=False)),
                ('reply_start_date', models.CharField(max_length=100)),
                ('reply_end_date', models.CharField(max_length=100)),
                ('company_yn', models.BooleanField(default=False)),
                ('department_yn', models.BooleanField(default=False)),
                ('reply_yn', models.BooleanField(default=False)),
                ('reply_date', models.CharField(max_length=100, null=True)),
                ('read', models.BooleanField(default=False)),
                ('trash', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='emails', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
