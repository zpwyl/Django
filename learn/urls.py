from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('home/', views.home, name='home'),
    path('home/<int:num>/', views.home, name='home'),
    path('home/<int:num>/<int:select_type>/', views.home, name='home'),
    path('home/<int:num>/<int:select_type>/<int:n>/', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('leyout/', views.leyout, name='leyout'),
    path('book_delete/<int:book_id>/', views.book_delete, name="book_delete"),
    path('book_update/<int:book_id>/', views.book_update, name="book_update"),
    path('user_update/<int:user_id>/', views.user_update, name="user_update"),
    path('borrow/<int:book_id>/', views.borrow, name="borrow"),
    path('returns/<int:book_id>/', views.returns, name="returns"),
    path('show_book/', views.show_book, name="show_book"),
    path('popup/', views.popup, name="popup"),
    path('get_yzm_img/', views.get_yzm_img, name="get_yzm_img"),
]