from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect, HttpResponse
from .form import LoginForm, BookForm, BooksForm, UserForm
from .models import User, Book, UserType, Borrow
import hashlib
import re
from datetime import datetime, timedelta
from django.http import HttpRequest
# Create your views here.


@csrf_exempt
def home(request:HttpRequest, num=None, select_type=None):
    try:
        v = request.session['name']
    except:
        v = None
    if num == None:
        return render(request, 'home.html', {'v': v})
    if num == 1:
        if select_type == None:
            n = 1
        else:
            n = select_type
        bok = Book.objects.all()
        #sum 获取总页数
        if len(bok) % 10:
            sum = len(bok)//10 + 1
        else:
            sum = len(bok)/10
        #n为当前页数
        books = Book.objects.filter(book_id__gte=(10*n)-9, book_id__lte=10*n)
        content = {
        'books': books,
        'num':num,
        'total_page': int(sum),
        'cur_page': n,
        'pre_page': n-1,
        'next_page': n+1,
            'v': v,
        }
        return render(request, 'home.html', content)
    if num == 2:
        if select_type == None:
            return render(request, 'home.html', {'num': num, 'select_type': select_type, 'v': v})
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
                                      {'num': num, 'select_type': select_type, 'message': '查无此书，请重新输入', 'v': v})
                    else:
                        return render(request, 'home.html', {'num': num, 'select_type': select_type, 'books': books, 'v': v})
            else:
                return render(request, 'home.html', {'num': num, 'select_type': select_type, 'v': v})
        if select_type == 2:
            if request.method == 'POST':
                sf = BookForm(request.POST)
                if sf.is_valid():
                    book_id = sf.cleaned_data['book_id']
                    try:
                        books = Book.objects.get(book_id=book_id)
                    except:
                        return render(request, 'home.html',
                                      {'num': num, 'select_type': select_type, 'message': '查无此书，请重新输入', 'v': v})
                    return render(request, 'home.html', {'num': num, 'select_type': select_type, 'books': books, 'v': v})

            else:
                return render(request, 'home.html', {'num': num, 'select_type': select_type, 'v': v})
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
                                      {'num': num, 'select_type': select_type, 'message': '查无此书，请重新输入', 'v': v})
                    return render(request, 'home.html', {'num': num, 'select_type': select_type, 'books': books, 'v': v})
            else:
                return render(request, 'home.html', {'num': num, 'select_type': select_type, 'v': v})
    if num == 3:
        if request.method == 'POST':
            bf = BooksForm(request.POST, request.FILES)
            # 表单信息输入不完整，输出默认值
            # post = dict(request.POST)
            # post.update({'book_price': ['30']})
            # bf = BookForm(post)
            # bf.book_price = 30
            if bf.is_valid():
                book_images = bf.cleaned_data['book_image']
                book_name = bf.cleaned_data['book_name']
                book_type = bf.cleaned_data['book_type']
                book_price = bf.cleaned_data['book_price']
                book_author = bf.cleaned_data['book_author']
                book_press = bf.cleaned_data['book_press']
                book_date = bf.cleaned_data['book_date']
                book_ISBN = bf.cleaned_data['book_ISBN']
                book_brief = bf.cleaned_data['book_brief']
                book_image = 'http://127.0.0.1:8000/media/' + str(book_images)
                books = []
                for book in Book.objects.all():
                    books.append(book.book_name)
                if book_name in books:
                    return render(request, 'home.html', {'num': num, 'message': '图书已存在', 'v': v})
                else:
                    Book.objects.create(book_name=book_name, book_type=book_type, book_price=book_price
                                        , book_author=book_author, book_press=book_press, book_date=book_date
                                        , book_ISBN=book_ISBN, book_brief=book_brief, book_image=book_image)
                    return render(request, 'home.html', {'num': num, 'message': '添加成功', 'v': v})
            else:
                return render(request, 'home.html', {'num': num, 'message': '添加书籍信息不完整', 'v': v})
        else:
            return render(request, 'home.html', {'num': num, 'v': v})
    if num == 4:
        books = []
        try:
            username = request.session['name']
            user = User.objects.get(username=username)
        except:
            return render(request, 'home.html', {'message': '请先登录'})
        else:
            borrows = Borrow.objects.all()
            for borrow in borrows:
                if borrow.userid == user:
                    books.append(borrow.book_id)
            if len(books) == 0:
                return render(request, 'home.html', {'num': num, 'message': '没有借书', 'v': v})
            else:
                if borrow.reDateAct:
                    return render(request, 'home.html',
                                  {'num': num, 'books': books, 'borrows': borrows, 'user': user, 'v': v,
                                   'message': '已还书'})
                return render(request, 'home.html', {'num': num, 'books': books, 'borrows': borrows, 'user': user, 'v': v})
    if num == 5:
        try:
            username = request.session['name']
            user = User.objects.get(username=username)
        except:
            return render(request, 'home.html', {'message': '请先登录'})
        else:
            return render(request, 'home.html', {'num': num, 'user': user, 'v': v})
    if num == 6:
        book = Book.objects.get(book_id=select_type)
        if request.method == 'POST':
            bsf = BooksForm(request.POST,request.FILES)
            if bsf.is_valid():
                book_images = bsf.cleaned_data['book_image']
                book.book_name = bsf.cleaned_data['book_name']
                book.book_price = bsf.cleaned_data['book_price']
                book.book_type = bsf.cleaned_data['book_type']
                book.book_author = bsf.cleaned_data['book_author']
                book.book_press = bsf.cleaned_data['book_press']
                book.book_date = bsf.cleaned_data['book_date']
                book.book_ISBN = bsf.cleaned_data['book_ISBN']
                book.book_brief = bsf.cleaned_data['book_brief']
                book.book_image = 'http://127.0.0.1:8000/media/' + str(book_images)
                book.save()
                return render(request, 'home.html', {'message': '修改成功', 'v': v})
            else:
                return render(request, 'home.html', {'num': num, 'message': '添加书籍信息不完整', 'v': v})
        return render(request, 'home.html', {'num': num, 'books': book, 'v': v})
    if num == 7:
        user = User.objects.get(userid=select_type)
        if request.method == 'POST':
            uf = UserForm(request.POST, request.FILES)
            if uf.is_valid():
                user.userphoto = uf.cleaned_data['userphoto']
                user.name = uf.cleaned_data['name']
                user.email = uf.cleaned_data['email']
                user.tel = uf.cleaned_data['tel']
                user.sex = uf.cleaned_data['sex']
                user.status = uf.cleaned_data['status']
                user.save()
                return render(request, 'home.html', {'num': num, 'message': '修改成功', 'v': v})
            else:
                return render(request, 'home.html', {'num': num, 'message': '添加书籍信息不完整', 'v': v})
        return render(request, 'home.html', {'num': num, 'user': user, 'v': v})


def borrow(request, book_id):
    book = Book.objects.get(book_id=book_id)
    try:
        username = request.session['name']
        user = User.objects.get(username=username)
    except:
        return render(request, 'home.html', {'message': '请先登录'})
    if Borrow.objects.filter(userid=user, book_id=book):
        return render(request, 'home.html', {'message': '该书已借', 'v': username})
    else:
        if user.borrownum < user.usertype.lendNum:
            ldDate = get_cur_date()
            reDatePlan = get_return_date()
            if book.book_status == 1:
                return render(request, 'home.html', {'message': '该书已被借', 'v': username})
            else:
                Borrow.objects.create(userid=user, book_id=book, ldDate=ldDate, reDatePlan=reDatePlan)
                book.book_status = 1
                user.borrownum += 1
                book.save()
                user.save()
                return render(request, 'home.html', {'message': '已成功借书', 'v': username})
        else:
            return render(request, 'home.html', {'message': '借书数量已达上限', 'v': username})


@csrf_exempt
def book_delete(request, book_id):
    if request.POST:
        Book.objects.get(book_id=book_id).delete()
        return render(request, 'home.html', {'message': '删除成功'})


def returns(request, book_id):
    book = Book.objects.get(book_id=book_id)
    try:
        username = request.session['name']
        user = User.objects.get(username=username)
    except:
        return render(request, 'home.html', {'message': '请先登录'})
    else:
        borrow = Borrow.objects.get(userid=user, book_id=book)
        borrow.reDateAct = get_cur_date()
        book.book_status = 0
        user.borrownum -= 1
        book.save()
        user.save()
        borrow.save()
        return render(request, 'home.html', {'message': '已成功还书', 'v': username})


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
                usertype = lf.cleaned_data['usertype']
                pwd = calc_md5(password)
                if User.objects.filter(username__exact=username, password__exact=pwd, usertype_id__exact=usertype):
                    user = User.objects.get(username__exact=username, password__exact=pwd)
                    request.session['name'] = user.username
                    #保存时间为一天
                    request.session.set_expiry(86400)
                    user.status = 1
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
        lf = LoginForm(request.POST)
        if lf.is_valid():
            use = []
            username = lf.cleaned_data['username']
            us = User.objects.all()
            for u in us:
                use.append(u.username)
            if username not in use:
                password = lf.cleaned_data['password']
                password1 = request.POST['password1']
                email = lf.cleaned_data['email']
                emails = is_valid_email(email)
                usertype = lf.cleaned_data['usertype']
                usertypes = UserType.objects.all()
                for ut in usertypes:
                    if int(usertype) == ut.usertype:
                        pass
                if emails == None:
                    return render(request, 'register.html', {'message':'邮箱格式输入错误'})
                if password == password1:
                    pwd = calc_md5(password)
                    User.objects.create(username=lf.cleaned_data['username'],
                                        password=pwd,
                                        email=emails,
                                        daterag=get_cur_date(),
                                        usertype=ut,
                                        borrownum=int(lf.cleaned_data['borrownum']),
                                        status=int(lf.cleaned_data['status']),)
                    return redirect('/')
                else:
                    return render(request, 'register.html', {'message': '两次密码输入不一致'})
            else:
                return render(request, 'register.html', {'message': '用户名已存在'})
        else:
            return render(request, 'register.html', {'message': '注册失败'})
    else:
        lf = LoginForm()
        return render(request, 'register.html', {'lf': lf})

def leyout(request):
    try:
        username = request.session['name']
        user = User.objects.get(username=username)
    except:
        return render(request, 'home.html', {'message': '请先登录'})
    else:
        user.status = 0
        user.save
        del request.session["name"]
        return render(request, 'home.html', {'message': '注销成功'})

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