# Generated by Django 5.1.1 on 2024-09-12 09:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('taapp', '0003_user_first_name_user_last_login_user_last_name'),
    ]

    operations = [
        migrations.DeleteModel(
            name='User',
        ),
    ]
