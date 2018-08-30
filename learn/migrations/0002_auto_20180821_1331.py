# Generated by Django 2.0.7 on 2018-08-21 05:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('learn', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Borrow',
            fields=[
                ('borrow_id', models.AutoField(primary_key=True, serialize=False)),
                ('ldContinueTimes', models.PositiveSmallIntegerField()),
                ('ldDate', models.CharField(max_length=20)),
                ('reDatePlan', models.CharField(max_length=20)),
                ('reDateAct', models.CharField(max_length=20)),
                ('ldOverDate', models.SmallIntegerField()),
                ('punishMonkey', models.IntegerField()),
                ('isHasReturn', models.PositiveSmallIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='UserType',
            fields=[
                ('usertype', models.SmallIntegerField(primary_key=True, serialize=False)),
                ('usertypeName', models.CharField(max_length=2)),
                ('lendNum', models.IntegerField()),
                ('lendDay', models.IntegerField()),
                ('continueTimes', models.IntegerField()),
                ('punishRate', models.FloatField()),
                ('dateVaild', models.IntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='book',
            name='book_ISBN',
            field=models.CharField(default=1, max_length=15),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='book',
            name='book_author',
            field=models.CharField(default=1, max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='book',
            name='book_brief',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='book',
            name='book_date',
            field=models.CharField(default=1, max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='book',
            name='book_image',
            field=models.ImageField(default=1, upload_to=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='book',
            name='book_press',
            field=models.CharField(default=1, max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='book',
            name='book_status',
            field=models.CharField(default=1, max_length=2),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='adminroles',
            field=models.PositiveSmallIntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='borrownum',
            field=models.PositiveSmallIntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='daterag',
            field=models.CharField(default=1, max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='name',
            field=models.CharField(default=1, max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='sex',
            field=models.CharField(default=1, max_length=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='status',
            field=models.PositiveSmallIntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='tel',
            field=models.CharField(default=1, max_length=11),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='userphoto',
            field=models.ImageField(default=1, upload_to=''),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=64),
        ),
        migrations.AddField(
            model_name='borrow',
            name='book_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='learn.Book'),
        ),
        migrations.AddField(
            model_name='borrow',
            name='userid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='learn.User'),
        ),
        migrations.AddField(
            model_name='user',
            name='usertype',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='learn.UserType'),
            preserve_default=False,
        ),
    ]
