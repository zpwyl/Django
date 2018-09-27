from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(label='用户名', max_length=32, empty_value='0')
    password = forms.CharField(label='密_码', max_length=30, empty_value='0')
    email = forms.CharField(label='邮箱', max_length=30, empty_value='0')
    usertype = forms.IntegerField(label='用户类型')
    borrownum = forms.CharField(label='借书数量', empty_value='0')
    status = forms.CharField(label='用户状态', empty_value='0')
    code = forms.CharField(label='验证码', empty_value='0')

class UserForm(forms.Form):
    userphoto = forms.FileField(label='图片', allow_empty_file='0.jpg')
    email = forms.EmailField(label='邮箱', max_length=30)
    name = forms.CharField(label='昵称', max_length=10)
    tel = forms.CharField(label='电话', max_length=11)
    sex = forms.CharField(label='性别', max_length=1)
    status = forms.IntegerField()

class BookForm(forms.Form):
    book_id = forms.CharField(label='图书编号', max_length=32, empty_value='0')
    book_name = forms.CharField(label='图书名称', max_length=30, empty_value='0')
    book_type = forms.CharField(label='图书类型', max_length=32, empty_value='0')
    book_price = forms.CharField(label='图书价格', max_length=30, empty_value='0')


class BooksForm(forms.Form):
    book_id = forms.CharField(label='图书编号', max_length=32, empty_value='0')
    book_name = forms.CharField(label='图书名称', max_length=30, empty_value='0')
    book_type = forms.CharField(label='图书类型', max_length=32, empty_value='0')
    book_price = forms.CharField(label='图书价格', max_length=30, empty_value='0')
    book_ISBN = forms.CharField(label='ISBN编号', max_length=15, empty_value='0')
    book_author = forms.CharField(label='图书作者', max_length=30, empty_value='0')
    book_brief = forms.CharField(label='图书简介', max_length=255, empty_value='0')
    book_date = forms.CharField(label='出版日期', max_length=20, empty_value='0')
    book_image = forms.FileField(allow_empty_file='0.jpg')
    book_press = forms.CharField(label='出版社', max_length=30, empty_value='0')