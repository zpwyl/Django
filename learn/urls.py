from django.urls import path

from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('home/', views.home, name='home'),
    path('home/<int:num>/', views.home, name='home'),
    path('home/<int:num>/<int:select_type>/', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('leyout/', views.leyout, name='leyout'),
    path('book_delete/<int:book_id>/', views.book_delete, name="book_delete"),
    path('borrow/<int:book_id>/', views.borrow, name="borrow"),
    path('returns/<int:book_id>/', views.returns, name="returns"),
]