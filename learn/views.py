from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, render_to_response, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from .form import LoginForm, RegisterForm, BookForm, BooksForm, UserForm
from .models import User, Book, UserType, Borrow
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import hashlib
import re
from datetime import datetime, timedelta
# Create your views here.


@csrf_exempt
def home(request, num=None, select_type=None):
    if num == None:
        return render(request, 'home.html')
    if num == 1:
        books = Book.objects.all()
        # for book in books:
        #     book.book_image
        return render(request, 'home.html', {'num': num, 'books': books, 'media':books})
    if num == 2:
        if select_type == None:
            return render(request, 'home.html', {'num': num, 'select_type': select_type})
        if select_type == 1:
            if request.method == 'POST':
                sf = BookForm(request.POST)
                if sf.is_valid():
                    book_name = sf.cleaned_data['book_name']
                    books = []
                    bf = Book.objects.all()
                    for b in bf:
                        if book_name == b.book_name:
                            books.append(b)
                    if len(books) == 0:
                        return render(request, 'home.html',
                                      {'num': num, 'select_type': select_type, 'message': '查无此书，请重新输入'})
                    else:
                        return render(request, 'home.html', {'num': num, 'select_type': select_type, 'books': books})
            else:
                return render(request, 'home.html', {'num': num, 'select_type': select_type})
        if select_type == 2:
            if request.method == 'POST':
                sf = BookForm(request.POST)
                if sf.is_valid():
                    book_id = sf.cleaned_data['book_id']
                    try:
                        books = Book.objects.get(book_id=book_id)
                    except:
                        return render(request, 'home.html',
                                      {'num': num, 'select_type': select_type, 'message': '查无此书，请重新输入'})
                    return render(request, 'home.html', {'num': num, 'select_type': select_type, 'books': books})

            else:
                return render(request, 'home.html', {'num': num, 'select_type': select_type})
        if select_type == 3:
            if request.method == 'POST':
                sf = BookForm(request.POST)
                if sf.is_valid():
                    book_type = sf.cleaned_data['book_type']
                    books = []
                    bf = Book.objects.all()
                    for b in bf:
                        if book_type == b.book_type:
                            books.append(b)
                    if len(books) == 0:
                        return render(request, 'home.html',
                                      {'num': num, 'select_type': select_type, 'message': '查无此书，请重新输入'})
                    return render(request, 'home.html', {'num': num, 'select_type': select_type, 'books': books})
            else:
                return render(request, 'home.html', {'num': num, 'select_type': select_type})
    if num == 3:
        if request.method == 'POST':
            bf = BooksForm(request.POST)
            # 表单信息输入不完整，输出默认值
            # post = dict(request.POST)
            # post.update({'book_price': ['30']})
            # bf = BookForm(post)
            # bf.book_price = 30
            book_image = 'http://127.0.0.1:8000/media/' + str(request.FILES.get('book_image'))
            if bf.is_valid():
                book_name = bf.cleaned_data['book_name']
                book_type = bf.cleaned_data['book_type']
                book_price = bf.cleaned_data['book_price']
                book_author = bf.cleaned_data['book_author']
                book_press = bf.cleaned_data['book_press']
                book_date = bf.cleaned_data['book_date']
                book_ISBN = bf.cleaned_data['book_ISBN']
                book_brief = bf.cleaned_data['book_brief']
                books = []
                for book in Book.objects.all():
                    books.append(book.book_name)
                if book_name in books:
                    return render(request, 'home.html', {'num': num, 'message': '图书已存在'})
                else:
                    Book.objects.create(book_name=book_name, book_type=book_type, book_price=book_price
                                        , book_author=book_author, book_press=book_press, book_date=book_date
                                        , book_ISBN=book_ISBN, book_brief=book_brief, book_image=book_image)
                    return render(request, 'home.html', {'num': num, 'message': '添加成功'})
            else:
                return render(request, 'home.html', {'num': num, 'message': '添加书籍信息不完整'})
        else:
            return render(request, 'home.html', {'num': num})
    if num == 4:
        books = []
        username = request.session['name']
        user = User.objects.get(username=username)
        borrows = Borrow.objects.all()
        for borrow in borrows:
            if borrow.userid == user:
                books.append(borrow.book_id)
        if len(books) == 0:
            return render(request, 'home.html', {'num': num, 'message': '没有借书'})
        else:
            return render(request, 'home.html', {'num': num, 'books': books, 'borrows': borrows, 'user': user})
    if num == 5:
        username = request.session['name']
        user = User.objects.get(username=username)
        return render(request, 'home.html', {'num': num, 'user': user})
    if num == 6:
        book = Book.objects.get(book_id=select_type)
        if request.method == 'POST':
            bsf = BooksForm(request.POST)
            book.book_image = 'http://127.0.0.1:8000/media/' + str(request.FILES.get('book_image'))
            if bsf.is_valid():
                book.book_name = bsf.cleaned_data['book_name']
                book.book_price = bsf.cleaned_data['book_price']
                book.book_type = bsf.cleaned_data['book_type']
                book.book_author = bsf.cleaned_data['book_author']
                book.book_press = bsf.cleaned_data['book_press']
                book.book_date = bsf.cleaned_data['book_date']
                book.book_ISBN = bsf.cleaned_data['book_ISBN']
                book.book_brief = bsf.cleaned_data['book_brief']
                book.save()
                return render(request, 'home.html', {'message': '修改成功'})
            else:
                return render(request, 'home.html', {'num': num, 'message': '添加书籍信息不完整'})
        return render(request, 'home.html', {'num': num, 'books': book})
    if num == 7:
        user = User.objects.get(userid=select_type)
        if request.method == 'POST':
            uf = UserForm(request.POST)
            user.userphoto = request.FILES.get('userphoto')
            if uf.is_valid():
                user.name = uf.cleaned_data['name']
                user.email = uf.cleaned_data['email']
                user.tel = uf.cleaned_data['tel']
                user.sex = uf.cleaned_data['sex']
                user.save()
                return render(request, 'home.html', {'num': num, 'message': '修改成功'})
            else:
                return render(request, 'home.html', {'num': num, 'message': '添加书籍信息不完整'})
        return render(request, 'home.html', {'num': num, 'user': user})


def borrow(request, book_id):
    book = Book.objects.get(book_id=book_id)
    username = request.session['name']
    user = User.objects.get(username=username)
    if Borrow.objects.filter(userid=user, book_id=book):
        return render(request, 'home.html', {'message': '该书已借'})
    else:
        if user.borrownum < user.usertype.lendNum:
            ldDate = get_cur_date()
            reDatePlan = get_return_date()
            Borrow.objects.create(userid=user, book_id=book, ldDate=ldDate, reDatePlan=reDatePlan)
            book.book_status = '借出'
            user.borrownum += 1
            book.save()
            user.save()
            return render(request, 'home.html', {'message': '已成功借书'})
        else:
            return render(request, 'home.html', {'message': '借书数量已达上限'})


@csrf_exempt
def book_delete(request, book_id):
    if request.POST:
        Book.objects.get(book_id=book_id).delete()
        return render(request, 'home.html', {'message':'删除成功'})


def returns(request, book_id):
    book = Book.objects.get(book_id=book_id)
    username = request.session['name']
    user = User.objects.get(username=username)
    Borrow.objects.filter(userid=user, book_id=book).delete()
    book.book_status = '在馆'
    user.borrownum -= 1
    book.save()
    user.save()
    return render(request, 'home.html', {'message': '已成功还书'})


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
                    user = User.objects.get(username__exact=username, password__exact=pwd)
                    request.session['name'] = user.username
                    user.save()
                    return redirect('/home/')
                else:
                    ErrorNum += 1
                    return render(request, 'login.html', {'message': '密码或用户名输入错误'})
            else:
                return render(request, 'login.html', {'message': '密码或用户名为空'})
        else:
            lf = LoginForm()
            return render(request, 'login.html', {'lf': lf})
    else:
        return HttpResponse('输入密码错误次数过多，稍后页面会跳转')


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
                    return render(request, 'register.html', {'message':'邮箱格式输入错误'})
                if password == password1:
                    pwd = calc_md5(password)
                    User.objects.create(username=rf.cleaned_data['username'],
                                        password=pwd,
                                        email=rf.cleaned_data['email'],
                                        daterag=get_cur_date())
                    return redirect('/')
                else:
                    return render(request, 'register.html', {'message': '两次密码输入不一致'})
            else:
                return render(request, 'register.html', {'message': '用户名已存在'})
        else:
            return render(request, 'register.html', {'message': '注册失败'})
    else:
        rf = RegisterForm()
        return render(request, 'register.html', {'rf': rf})


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


def get_cur_date():
    dt = datetime.now()
    cur_date = dt.strftime('%Y-%m-%d')
    return cur_date

def get_return_date():
    dt = datetime.now()
    cur_date = dt + timedelta(days=10)
    returnDate = cur_date.strftime('%Y-%m-%d')
    return returnDate


