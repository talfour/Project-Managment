# Generated by Django 3.2.5 on 2021-08-17 14:48

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_alter_crew_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='crew',
            name='date_added',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
