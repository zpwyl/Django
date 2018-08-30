from django.db import models


class UserType(models.Model):
    usertype = models.SmallIntegerField(primary_key=True)
    usertypeName = models.CharField(max_length=2)
    lendNum = models.IntegerField()
    lendDay = models.IntegerField()
    continueTimes = models.IntegerField()
    punishRate = models.FloatField()
    dateVaild = models.IntegerField()


class User(models.Model):
    userid = models.AutoField(primary_key=True)
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=64)
    email = models.EmailField(max_length=30)
    name = models.CharField(max_length=10)
    sex = models.CharField(max_length=1)
    usertype = models.ForeignKey('UserType', on_delete=models.CASCADE)
    tel = models.CharField(max_length=11)
    daterag = models.CharField(max_length=20)
    userphoto = models.ImageField(upload_to='', default="0.jpg")
    status = models.PositiveSmallIntegerField()
    borrownum = models.PositiveSmallIntegerField()


class Book(models.Model):
    book_id = models.AutoField(primary_key=True)
    book_name = models.CharField(max_length=30)
    book_type = models.CharField(max_length=32)
    book_price = models.CharField(max_length=30)
    book_author = models.CharField(max_length=30)
    book_press = models.CharField(max_length=30)
    book_date = models.CharField(max_length=10)
    book_ISBN = models.CharField(max_length=15)
    book_brief = models.CharField(max_length=255)
    book_image = models.ImageField(upload_to='', default="0.jpg")
    book_status = models.CharField(max_length=2, default="0")


class Borrow(models.Model):
    borrow_id = models.AutoField(primary_key=True)
    userid = models.ForeignKey('User', on_delete=models.CASCADE)
    book_id = models.ForeignKey('Book', on_delete=models.CASCADE)
    ldContinueTimes = models.PositiveSmallIntegerField()
    ldDate = models.CharField(max_length=20)
    reDatePlan = models.CharField(max_length=20)
    reDateAct = models.CharField(max_length=20)
    ldOverDate = models.SmallIntegerField()
    punishMonkey = models.IntegerField()
    isHasReturn = models.PositiveSmallIntegerField()
