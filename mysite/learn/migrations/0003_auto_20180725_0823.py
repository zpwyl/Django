# Generated by Django 2.0.7 on 2018-07-25 00:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learn', '0002_remove_user_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=32),
        ),
    ]
