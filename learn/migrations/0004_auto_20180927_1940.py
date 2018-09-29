# Generated by Django 2.1.1 on 2018-09-27 11:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('learn', '0003_auto_20180831_0832'),
    ]

    operations = [
        migrations.CreateModel(
            name='History',
            fields=[
                ('History_id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=20)),
                ('book_name', models.CharField(max_length=90)),
                ('overdue_days', models.CharField(max_length=20)),
                ('punishMonkey', models.IntegerField()),
                ('reDateAct', models.CharField(max_length=20)),
                ('ldDate', models.CharField(max_length=20)),
                ('book_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='learn.Book')),
            ],
        ),
        migrations.RemoveField(
            model_name='borrow',
            name='isHasReturn',
        ),
        migrations.RemoveField(
            model_name='borrow',
            name='ldContinueTimes',
        ),
        migrations.RemoveField(
            model_name='borrow',
            name='ldOverDate',
        ),
        migrations.RemoveField(
            model_name='borrow',
            name='reDateAct',
        ),
        migrations.AlterField(
            model_name='user',
            name='sex',
            field=models.PositiveSmallIntegerField(),
        ),
        migrations.AddField(
            model_name='history',
            name='userid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='learn.User'),
        ),
    ]