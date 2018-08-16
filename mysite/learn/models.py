from django.db import models


class User(models.Model):
    userid = models.AutoField(primary_key=True)
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=30)
    email = models.EmailField(max_length=30)


class Book(models.Model):
     book_id = models.AutoField(primary_key=True)
     book_name = models.CharField(max_length=30)
     book_type = models.CharField(max_length=32)
     book_price = models.CharField(max_length=30)


