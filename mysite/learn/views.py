from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .form import LoginForm, RegisterForm, BookForm
from .models import User, Book
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import hashlib
import re


# Create your views here.
@csrf_exempt
@login_required(login_url='/login/')
def home(request, num=None, select_type=None):
    if num == None:
        return render(request, 'home.html', message('欢迎来到图书馆系统!!!'))
    if num == 1:
        books = Book.objects.all()
        paginator = Paginator(books, 5)
        page = request.GET.get('page')
        try:
            books = paginator.page(page)
        except PageNotAnInteger:
            books = paginator.page(1)
        except EmptyPage:
            books = paginator.page(paginator.num_pages)
        return render(request, 'home.html', {'num': num, 'books': books})

    if num == 2:
        if select_type == None:
            return render(request, 'home.html', {'num': num, 'select_type': select_type})
        if select_type == 1:
            if request.method == 'POST':
                sf = BookForm(request.POST)
                if sf.is_valid():
                    book_name = sf.cleaned_data['book_name']
                    bfs = []
                    bf = Book.objects.all()
                    try:
                        for b in bf:
                            if book_name == b.book_name:
                                bfs.append(b)
                    except:
                        return render(request, 'home.html', {'num': num, 'select_type': select_type, 'messages': '查无此书，请重新输入'})
                    return render(request, 'home.html', {'num': num, 'select_type': select_type, 'result': bfs})
                else:
                    return render(request, 'home.html', {'num': num, 'select_type': select_type, 'messages': '输入为空，请输入书名！'})
            else:
                return render(request, 'home.html', {'num': num, 'select_type': select_type})
        if select_type == 2:
            if request.method == 'POST':
                sf = BookForm(request.POST)
                if sf.is_valid():
                    book_id = sf.cleaned_data['book_id']
                    try:
                        bfs = Book.objects.get(book_id=book_id)
                    except :
                        return render(request, 'home.html', {'num': num, 'select_type': select_type, 'messages': '查无此书，请重新输入'})
                    return render(request, 'home.html', {'num': num, 'select_type': select_type, 'result': bfs})
                else:
                    return render(request, 'home.html', {'num': num, 'select_type': select_type, 'messages': '输入为空，请输入书名！'})
            else:
                return render(request, 'home.html', {'num': num, 'select_type': select_type})
        if select_type == 3:
            if request.method == 'POST':
                sf = BookForm(request.POST)
                if sf.is_valid():
                    book_type = sf.cleaned_data['book_type']
                    books = []
                    bf = Book.objects.all()
                    try:
                        for b in bf:
                            if book_type == b.book_type:
                                books.append(b)
                    except:
                        return render(request, 'home.html', {'num': num, 'select_type': select_type, 'messages': '查无此书，请重新输入'})
                    return render(request, 'home.html', {'num': num, 'select_type': select_type, 'books': books})
                else:
                    return render(request, 'home.html', {'num': num, 'select_type': select_type, 'messages':'输入为空，请输入书名！'})
            else:
                return render(request, 'home.html', {'num': num, 'select_type': select_type})

    if num == 3:
        if request.method == 'POST':
            bf = BookForm(request.POST)
            #表单信息输入不完整，输出默认值
            # post = dict(request.POST)
            # post.update({'book_price': ['30']})
            # bf = BookForm(post)
            # bf.book_price = 30
            if bf.is_valid():
                book_name = bf.cleaned_data['book_name']
                book_type = bf.cleaned_data['book_type']
                book_price = bf.cleaned_data['book_price']
                if book_name in Book.objects.all().values('book_name'):
                    return render(request, 'home.html', messages(num, '图书已存在'))
                else:
                    Book.objects.create(book_name=book_name, book_type=book_type, book_price=book_price)
                    return render(request, 'home.html', messages(num, '添加成功'))
            else:
                return render(request, 'home.html', messages(num, '添加书籍信息不完整'))
        else:
            return render(request, 'home.html', {'num': num})

    if num == 5:
        book = Book.objects.get(book_id=select_type)
        if request.method == 'POST':
            bf = BookForm(request.POST)
            if bf.is_valid():
                book_name = bf.cleaned_data['book_name']
                book_price = bf.cleaned_data['book_price']
                book.book_name = book_name
                book.book_price = book_price
                book.save()
                return render(request, 'home.html',  {'num': num})
            else:
                return render(request, 'home.html', messages(num, '添加书籍信息不完整'))
        return render(request, 'home.html', {'num': num, 'books': book})


@csrf_exempt
def book_delete(request, book_id):
    if request.POST:
        Book.objects.get(book_id=book_id).delete()
        return render(request, 'home.html', message('删除成功'))


@csrf_exempt
def register(request):
    if request.method == 'POST':
        rf = RegisterForm(request.POST)
        if rf.is_valid():
            use = []
            username = rf.cleaned_data['username']
            us = User.objects.all()
            for u in us:
                use.append(u.username)
            if username not in use:
                password = rf.cleaned_data['password']
                password1 = request.POST['password1']
                email = rf.cleaned_data['email']
                emails = is_valid_email(email)
                if emails == None:
                    return render(request, 'register.html', message("邮箱格式输入错误"))
                if password == password1:
                    pwd = calc_md5(password)
                    User.objects.create(username=rf.cleaned_data['username'],
                                        password=pwd,
                                        email=rf.cleaned_data['email'])
                    return redirect('/')
                else:
                    return render(request, 'register.html', message("两次密码输入不一致"))
            else:
                return render(request, 'register.html', message("用户名已存在"))
        else:
            return render(request, 'register.html', message('注册失败'))
    else:
        rf = RegisterForm()
        return render(request, 'register.html')


ErrorNum = 0


@csrf_exempt
def login(request):
    global ErrorNum
    if ErrorNum <= 3:
        if request.method == 'POST':
            lf = LoginForm(request.POST)
            if lf.is_valid():
                username = lf.cleaned_data['username']
                password = lf.cleaned_data['password']
                pwd = calc_md5(password)
                if User.objects.filter(username__exact=username, password__exact=pwd):
                    return redirect('/home/')
                else:
                    ErrorNum += 1
                    return render(request, 'login.html', message('密码或用户名输入错误'))
            else:
                return render(request, 'login.html', message('密码或用户名为空'))
        else:
            lf = LoginForm()
            return render(request, 'login.html', {'lf': lf})
    else:
        return HttpResponse('输入密码错误次数过多，稍后页面会跳转')

#通过摘要算法对密码加密
def calc_md5(password):
    md5 = hashlib.md5()
    key = 'zp'
    pwds = key + password
    md5.update(pwds.encode('utf-8'))
    pwd = md5.hexdigest()
    return pwd

#验证邮箱
def is_valid_email(email):
    try:
        m = re.match(r'^[a-zA-Z0-9_.-]+@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*\.[a-zA-Z0-9]{2,6}$', email).group()
    except:
        m = None
    else:
        return m

def message(message):
    return {'message': message}


def messages(num, messages):
    return {'num': num, 'messages': messages}


