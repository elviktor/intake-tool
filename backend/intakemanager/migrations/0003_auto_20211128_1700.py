# Generated by Django 3.1 on 2021-11-28 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('intakemanager', '0002_auto_20211128_1653'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='intakeuser',
            options={'ordering': ['last_name']},
        ),
        migrations.AddField(
            model_name='intakeuser',
            name='schedule',
            field=models.URLField(blank=True),
        ),
    ]
