# Generated by Django 3.2.5 on 2021-07-30 11:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0003_auto_20210728_2029'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tag',
            name='task',
        ),
        migrations.AlterField(
            model_name='task',
            name='priority',
            field=models.CharField(choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')], default='low', max_length=15),
        ),
        migrations.AlterField(
            model_name='task',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='project.project'),
        ),
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.CharField(choices=[('complete', 'Complete'), ('in_progress', 'In progress'), ('not_started', 'Not started'), ('on_hold', 'On hold')], default='not_started', max_length=11),
        ),
        migrations.DeleteModel(
            name='Section',
        ),
        migrations.DeleteModel(
            name='Tag',
        ),
    ]
