from django.contrib import admin

# Register your models here.
from .models import User, Book, UserType, Borrow

admin.site.register(User)

admin.site.register(Book)

admin.site.register(UserType)

admin.site.register(Borrow)