# Generated by Django 3.2.5 on 2021-07-27 18:02

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='crew',
            name='user',
            field=models.ManyToManyField(related_name='crew', to=settings.AUTH_USER_MODEL),
        ),
    ]