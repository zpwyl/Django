from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(label='用户名', max_length=32)
    password = forms.CharField(label='密_码', max_length=30)


class RegisterForm(forms.Form):
    username = forms.CharField(label='用户名', max_length=32)
    password = forms.CharField(label='密_码', max_length=30)
    email = forms.CharField(label='邮箱', max_length=30)


class BookForm(forms.Form):
    book_id = forms.CharField(label='图书编号', max_length=32, empty_value='0')
    book_name = forms.CharField(label='书名', max_length=32, empty_value='0')
    book_type = forms.CharField(label='图书类型', max_length=32, empty_value='0')
    book_price = forms.CharField(label='图书价格', max_length=32, empty_value='0')