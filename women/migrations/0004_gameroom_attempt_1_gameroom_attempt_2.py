# Generated by Django 4.1.3 on 2023-02-05 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('women', '0003_gameroom'),
    ]

    operations = [
        migrations.AddField(
            model_name='gameroom',
            name='attempt_1',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='gameroom',
            name='attempt_2',
            field=models.IntegerField(default=0),
        ),
    ]
