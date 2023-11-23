# Generated by Django 4.1.12 on 2023-11-23 11:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_coach_alter_teamtable_coachs'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='teamtable',
            name='coachs',
        ),
        migrations.AddField(
            model_name='coach',
            name='teams',
            field=models.ManyToManyField(blank=True, related_name='teams', to='dashboard.teamtable'),
        ),
    ]