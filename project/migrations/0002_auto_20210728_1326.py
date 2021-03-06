# Generated by Django 3.2.5 on 2021-07-28 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='project',
            options={'ordering': ['-created_at']},
        ),
        migrations.AddField(
            model_name='project',
            name='slug',
            field=models.SlugField(default='test', max_length=80, unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='task',
            name='priority',
            field=models.CharField(choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')], default=-1, max_length=15),
        ),
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.CharField(choices=[('complete', 'Complete'), ('in_progress', 'In progress'), ('not_started', 'Not started'), ('on_hold', 'On hold')], default=1, max_length=11),
        ),
    ]
