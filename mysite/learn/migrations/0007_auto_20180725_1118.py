# Generated by Django 2.0.7 on 2018-07-25 03:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learn', '0006_auto_20180725_1116'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='id',
        ),
        migrations.AddField(
            model_name='user',
            name='userid',
            field=models.AutoField(default=1, primary_key=True, serialize=False),
            preserve_default=False,
        ),
    ]
