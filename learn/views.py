from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from .form import LoginForm, BookForm, BooksForm, UserForm
from .models import User, Book, UserType, Borrow, History
from .function import *
from django.http import HttpRequest, JsonResponse
from jieba import posseg, analyse
import math
from operator import itemgetter
# Create your views here.


@csrf_exempt
def home(request: HttpRequest, num=1, select_type=1):
    try:
        username = request.session['name']
        user = User.objects.get(username=username)
    except:
        return redirect('/')
    if user.usertype.usertype == 4:
        if num == 1:
            n = select_type
            bok = Book.objects.all()
            #sum 获取总页数
            if len(bok) % 10:
                sum = len(bok)//10 + 1
            else:
                sum = len(bok)/10
            #n为当前页数
            start = 10*(n-1)
            end = 10*n
            books = Book.objects.all().order_by('book_id')[start:end]
            rec = []
            for book in books:
                rec.append(book.book_id)
            content = {
                'books': books,
                'num': num,
                'total_page': int(sum),
                'cur_page': n,
                'pre_page': n-1,
                'next_page': n+1,
                'user': user,
            }
            return render(request, 'home.html', content)
        if num == 2:
            if select_type == 1:
                if request.method == 'POST':
                    sf = BookForm(request.POST)
                    if sf.is_valid():
                        book_name = sf.cleaned_data['book_name']
                        request.session['book_name'] = book_name
                        return redirect('/show_book/')
                content = {
                    'num': num,
                    'select_type': select_type,
                    'user': user,
                }
                return render(request, 'home.html', content)
            if select_type == 2:
                if request.method == 'POST':
                    sf = BookForm(request.POST)
                    if sf.is_valid():
                        book_id = sf.cleaned_data['book_id']
                        request.session['book_id'] = book_id
                        return redirect('/show_book/')
                content = {
                    'num': num,
                    'select_type': select_type,
                    'user': user,
                }
                return render(request, 'home.html', content)
        if num == 3:
            a = locals()
            print(a)
            if request.method == 'POST':
                bf = BooksForm(request.POST, request.FILES)
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
                    book_image = '/media/' + str(book_images)
                    books = []
                    for book in Book.objects.all():
                        books.append(book.book_name)
                    if book_name in books:
                        content = {
                            'num': 2,
                            'message': '图书已存在',
                        }
                        return render(request, 'popup.html', content)
                    else:
                        Book.objects.create(book_name=book_name, book_type=book_type, book_price=book_price
                                            , book_author=book_author, book_press=book_press, book_date=book_date
                                            , book_ISBN=book_ISBN, book_brief=book_brief, book_image=book_image)
                        content = {
                            'num': 2,
                            'message': '添加成功',
                        }
                        return render(request, 'popup.html', content)
                else:
                    content = {
                        'num': 2,
                        'message': '添加书籍信息不完整',
                    }
                    return render(request, 'popup.html', content)
            else:
                content = {
                    'num': num,
                    'user': user,
                }
                return render(request, 'home.html', content)
        if num == 4:
            n = select_type
            start = 10 * (n - 1)
            end = 10 * n
            bok = History.objects.all()
            # sum 获取总页数
            if len(bok) % 10:
                sum = len(bok) // 10 + 1
            else:
                sum = len(bok) / 10
            history = History.objects.all()[start: end]
            if len(history) == 0:
                return render(request, 'popup.html', {'message': '没有借书记录', 'num': 1})
            content = {
                'num': num,
                'cur_page': n,
                'pre_page': n-1,
                'next_page': n+1,
                'total_page': int(sum),
                'user': user,
                'history': history,
            }
            return render(request, 'home.html', content)
        if num == 5:
            username = request.session['name']
            user = User.objects.get(username=username)
            users = User.objects.all()[0:10]
            content = {
                'num': num,
                'users': users,
                'user': user,
            }
            return render(request, 'home.html', content)
    else:
        if num == 1:
            n = select_type
            bok = Book.objects.all()
            # sum 获取总页数
            if len(bok) % 10:
                sum = len(bok) // 10 + 1
            else:
                sum = len(bok) / 10
            # n为当前页数
            start = 10 * (n - 1)
            end = 10 * n
            books = Book.objects.all()[start:end]
            rec = []
            for book in books:
                rec.append(book.book_id)
            # recommend_books = recommend(rec)
            # reconnend_users = reconnendUser(user.userid)
            # reconnend_books = reconnendBook(n)
            content = {
                'books': books,
                'num': num,
                'total_page': int(sum),
                'cur_page': n,
                'pre_page': n - 1,
                'next_page': n + 1,
                'user': user,
                # 'recommend_books': recommend_books,
                # 'reconnend_users': reconnend_users,
                # 'reconnend_books': reconnend_books,
            }
            return render(request, 'home.html', content)
        if num == 2:
            if select_type == 1:
                if request.method == 'POST':
                    sf = BookForm(request.POST)
                    if sf.is_valid():
                        book_name = sf.cleaned_data['book_name']
                        request.session['book_name'] = book_name
                        return redirect('/show_book/')
                content = {
                    'num': num,
                    'select_type': select_type,
                    'user': user,
                }
                return render(request, 'home.html', content)
            if select_type == 2:
                if request.method == 'POST':
                    sf = BookForm(request.POST)
                    if sf.is_valid():
                        book_id = sf.cleaned_data['book_id']
                        request.session['book_id'] = book_id
                        return redirect('/show_book/')
                content = {
                    'num': num,
                    'select_type': select_type,
                    'user': user,
                }
                return render(request, 'home.html', content)
        if num == 3:
            warning = []
            borrows = Borrow.objects.filter(userid=user.userid)
            if len(borrows) == 0:
                return render(request, 'popup.html', {'message': '当前没有借书', 'num': 1})
            else:
                for borrow in borrows:
                    a = int((get_over_day(borrow.reDatePlan) - get_over_day(get_cur_date())).days)
                    if a < 2:
                        warning.append(borrow)
                if len(borrow) == 0:
                    return render(request, 'popup.html', {'message': '当前没有欠费警告', 'num': 1})
                else:
                    return render(request, 'home.html', {'num': num, 'warning': warning, 'user': user})
        if num == 4:
            books = []
            borrows = Borrow.objects.all()
            for borrow in borrows:
                if borrow.userid == user:
                    books.append(borrow.book_id)
            if len(books) == 0:
                return render(request, 'popup.html', {'message': '没有借书', 'num': 1})
            content = {
                'num': num,
                'books': books,
                'borrows': borrows,
                'user': user,
            }
            return render(request, 'home.html', content)
        if num == 5:
            username = request.session['name']
            user = User.objects.get(username=username)
            content = {
                'num': num,
                'user': user,
            }
            return render(request, 'home.html', content)


def popup(request, message, num=1):
    return render(request, 'popup.html', {'num': num, 'message': message})


def show_book(request):
    username = request.session['name']
    user = User.objects.get(username=username)
    try:
        book_name = request.session['book_name']
        del request.session["book_name"]
    except:
        book_name = None
    try:
        book_id = request.session['book_id']
        del request.session["book_id"]
    except:
        book_id = None
    books = []
    bf = Book.objects.all()
    if book_name != None:
        for b in bf:
            if book_name == b.book_name:
                books.append(b)
    else:
        for b in bf:
            if int(book_id) == b.book_id:
                books.append(b)
    if len(books) == 0:
        content = {
            'num': 2,
            'message': '查无此书，请重新输入',
        }
        return render(request, 'popup.html', content)
    else:
        content = {
            'books': books,
            'user': user,
        }
        return render(request, 'show_book.html', content)


@csrf_exempt
def user_update(request, user_id):
    user = User.objects.get(userid=user_id)
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
            return render(request, 'popup.html', {'message': '修改成功', 'num': 5})
        else:
            return render(request, 'user_update.html', {'message': '添加信息不完整'})
    return render(request, 'user_update.html', {'user': user})


@csrf_exempt
def book_update(request, book_id):
    username = request.session['name']
    user = User.objects.get(username=username)
    book = Book.objects.get(book_id=book_id)
    if request.method == 'POST':
        bsf = BooksForm(request.POST, request.FILES)
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
            book.book_image = '/media/' + str(book_images)
            book.save()
            return render(request, 'book_update.html', {'message': '修改成功'})
        else:
            return render(request, 'book_update.html', {'message': '添加书籍信息不完整'})
    return render(request, 'book_update.html', {'books': book, 'user': user})


def borrow(request, book_id):
    book = Book.objects.get(book_id=book_id)
    username = request.session['name']
    user = User.objects.get(username=username)
    if Borrow.objects.filter(userid=user, book_id=book):
        return render(request, 'popup.html', {'message': '已借该书', 'num': 1})
    else:
        if user.borrownum < user.usertype.lendNum:
            ldDate = get_cur_date()
            reDatePlan = get_return_date()
            if book.book_status == 1:
                return render(request, 'popup.html', {'message': '该书已被借', 'num': 1})
            else:
                Borrow.objects.create(userid=user, book_id=book, ldDate=ldDate, reDatePlan=reDatePlan, punishMonkey=0)
                book.book_status = 1
                user.borrownum += 1
                book.save()
                user.save()
                return render(request, 'popup.html', {'message': '已成功借书', 'num': 1})
        else:
            return render(request, 'popup.html', {'message': '借书数量已达上限', 'num': 1})


@csrf_exempt
def book_delete(request, book_id):
    if request.POST:
        Book.objects.get(book_id=book_id).delete()
        return render(request, 'popup.html', {'message': '删除成功', 'num': 1})


def returns(request, book_id):
    book = Book.objects.get(book_id=book_id)
    try:
        username = request.session['name']
        user = User.objects.get(username=username)
    except:
        return redirect('/')
    else:
        borrow = Borrow.objects.get(userid=user, book_id=book)
        book.book_status = 0
        user.borrownum -= 1
        book.save()
        user.save()
        borrow.delete()
        ldDate = borrow.ldDate
        reDateAct = get_cur_date()
        overdue_date = (get_over_day(reDateAct) - get_over_day(borrow.reDatePlan)).days
        if overdue_date < 0:
            overdue_date = 0
        punishMonkey = borrow.punishMonkey
        if punishMonkey > 0:
            # 未完成
            return render(request, 'popup.html', {'message': '请先还完欠款', 'num': 4})
        else:
            History.objects.create(userid=user,book_id=book,username=user.name,ldDate=ldDate,book_name=book.book_name,reDateAct=reDateAct,overdue_days=overdue_date, punishMonkey=punishMonkey)
            return render(request, 'popup.html', {'message': '已成功还书', 'num': 4})


# 付款
def pay(request):
    pass


ErrorNum = 0
n = 0


def get_yzm_img(request):
    global n
    n += 1
    yzm_object = get_yzm('', 100, 40)
    yzm = yzm_object.get_yzm()
    request.session['yzm'] = yzm
    return redirect('/')


@csrf_exempt
def login(request):
    global n
    if n == 0:
        return redirect('/get_yzm_img/')
    else:
        global ErrorNum
        if ErrorNum <= 3:
            if request.method == 'POST':
                lf = LoginForm(request.POST)
                if lf.is_valid():
                    username = lf.cleaned_data['username']
                    password = lf.cleaned_data['password']
                    usertype = lf.cleaned_data['usertype']
                    code = lf.cleaned_data['code']
                    pwd = calc_md5(password)
                    yzm1 = request.session['yzm']
                    if code.lower() == yzm1.lower():
                        if User.objects.filter(username__exact=username, password__exact=pwd, usertype_id__exact=usertype):
                            user = User.objects.get(username__exact=username, password__exact=pwd)
                            request.session['name'] = user.username
                            #保存时间为一天
                            request.session.set_expiry(86400)
                            user.status = 1
                            user.save()
                            borrows = Borrow.objects.filter(userid=user.userid)
                            for borrow in borrows:
                                overdue_date = (get_over_day(get_cur_date()) - get_over_day(borrow.reDatePlan)).days
                                punishMonkey = overdue_date * user.usertype.punishRate
                                if punishMonkey > 0:
                                    borrow.punishMonkey = punishMonkey
                                else:
                                    borrow.punishMonkey = 0
                                borrow.save()
                            return redirect('/home/')
                        else:
                            ErrorNum += 1
                            return render(request, 'login.html', {'message': '密码或用户名输入错误'})
                    else:
                        return render(request, 'login.html', {'message': '验证码输入错误'})
                else:
                    return render(request, 'login.html', {'message': '密码或用户名为空'})
            else:
                lf = LoginForm()
                return render(request, 'login.html', {'lf': lf})
        else:
            return render(request, 'popup.html', {'message': '输入密码错误次数过多，稍后页面会跳转'})


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
                print(usertype)
                for ut in usertypes:
                    if usertype == ut.usertype:
                        break
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


@csrf_exempt
def leyout(request):
    try:
        username = request.session['name']
        user = User.objects.get(username=username)
    except:
         return redirect('/')
    else:
        global n
        n = 0
        user.status = 0
        user.save
        del request.session["name"]
        return redirect('/')


def show_books(request, book_id):
    username = request.session['name']
    user = User.objects.get(username=username)
    book = Book.objects.get(book_id=book_id)
    return render(request, 'show_book.html', {'book': book, 'user': user})


# 获取最热推荐
def recommend(recommend_book):
    books_info = {}
    res = History.objects.values_list('userid_id', 'book_id_id')
    for i, j in res:
        books_info.setdefault(i, [])
        books_info[i].append(j)
    users = []
    for user, goods in books_info.items():
        for good in goods:
            if good in recommend_book:
                users.append(user)
    books_id = {}
    for user in users:
        book_id = books_info[user]
        for book in book_id:
            if book in recommend_book:
                continue
            else:
                books_id.setdefault(book, 0)
                books_id[book] += 1
    results = sorted(books_id.items(), key=itemgetter(1), reverse=True)[:4]
    result = []
    for res in results:
        result.append(Book.objects.get(book_id=res[0]))
    return result


# 获取猜你喜欢(用户相似度)
def reconnendUser(userId):
    user_goods_info = {}
    res = History.objects.values_list('userid_id', 'book_id_id')
    for i, j in res:
        user_goods_info.setdefault(i, [])
        user_goods_info[i].append(j)
    goods_user_info={}
    user_inter_info={}
    user_similar_info={}

    for u, goods in user_goods_info.items():
        for good in goods:
            if good not in goods_user_info:
                goods_user_info.setdefault(good, set())
            else:
                pass
            goods_user_info[good].add(u)

    #用户之间购买商品的交集
    for gds, users in goods_user_info.items():
        for u in users:
            for v in users:
                if u == v:
                    continue
                if u not in user_inter_info:
                    user_inter_info.setdefault(u,{})
                if v not in user_inter_info[u]:
                    user_inter_info[u][v]=0
                user_inter_info[u][v] += 1

    for u, uc in user_inter_info.items():
        for v, inter in uc.items():
            if u not in user_similar_info:
                user_similar_info.setdefault(u, {})
            if v not in user_similar_info[u]:
                user_similar_info[u][v] = 0
            user_similar_info[u][v] = inter / math.sqrt(len(user_goods_info[u]) * len(user_goods_info[v]))
    shopGoods = user_goods_info[userId]
    recommendGoods = {}
    for u, uc in sorted(user_similar_info[userId].items(), key=itemgetter(1), reverse=True)[:20]:
        for gds in user_goods_info[u]:
            if gds in shopGoods:
                continue
            if gds not in recommendGoods:
                recommendGoods.setdefault(gds, 0)
            recommendGoods[gds] += uc

    results = sorted(recommendGoods.items(), key=itemgetter(1), reverse=True)[:8]
    result = []
    for res in results:
        result.append(Book.objects.get(book_id=res[0]))
    return result


# 获取看了还看(内容相似度)
def reconnendBook(n):
    results = Book.objects.values_list('book_id', 'book_name', 'book_type', 'book_author', 'book_press', 'book_brief')
    # 获取图书的书名标题简介等信息
    book_info = {}
    for res in results:
        book_info.setdefault(res[0], [])
        book_info[res[0]] = res[1] + res[2] + res[3] + res[4] + res[5]

    # 获取停用词
    stop_words = []
    with open('static/txt/stop_words.txt', 'rb') as sw:
        stop_words = sw.readlines()

    # 获取当前页面十本书信息的关键字
    rec_book_info = {}
    start = 10*(n-1)
    end = 10*n
    results = Book.objects.values_list('book_id', 'book_name', 'book_type', 'book_author', 'book_press', 'book_brief')[start: end]
    for res in results:
        rec_book_info.setdefault(res[0], [])
        rec_book_info[res[0]] = res[1] + res[2] + res[3] + res[4] + res[5]

    key_words = []
    for kbn, word in rec_book_info.items():
        words = posseg.cut(word)
        for wds in words:
            if wds.flag.startswith('n') and wds.word not in stop_words:
                key_words.append(wds.word)
    resultWord = analyse.extract_tags(str(key_words), topK=10)

    # 获取其他每一本书籍信息的关键字
    other_book_words = {}
    sum = len(Book.objects.all())
    if start < 100:
        start = 0
        end = end+100
    elif start >= 100 and end <= sum-100:
        start = start - 100
        end = end + 100
    elif end > sum-100:
        start = start-100
        end = sum
    for bkn, oword in book_info.items():
        if bkn in range(10*(n-1), 10*n):
            continue
        else:
            if bkn in range(start, end+1):
                keys = []
                owords = posseg.cut(oword)
                for owds in owords:
                    if owds.flag.startswith('n') and owds.word not in stop_words:
                        keys.append(owds.word)
                if bkn not in other_book_words:
                    other_book_words.setdefault(bkn, [])
                other_book_words[bkn] = analyse.extract_tags(str(keys), topK=10)


    # 比较前十本书籍和其他每本书籍的关键字的相似度
    recommendGoods = {}
    for bkn, r in other_book_words.items():
        if bkn not in recommendGoods:
            recommendGoods.setdefault(bkn, 0)
        recommendGoods[bkn] = len(set(r) & set(resultWord)) / len(resultWord)

    results = sorted(recommendGoods.items(), key=itemgetter(1), reverse=True)[:8]
    result = []
    for res in results:
        result.append(Book.objects.get(book_id=res[0]))
    return result


@csrf_exempt
def get_recommend(request, n):
    start = 10 * (n - 1)
    end = 10 * n
    books = Book.objects.all()[start:end]
    rec = []
    for book in books:
        rec.append(book.book_id)
    recommend_book = recommend(rec)
    recommend_books = []
    for recom in recommend_book:
        recommend_books.append([recom.book_name, str(recom.book_image), recom.book_id])
    return JsonResponse(recommend_books, safe=False)


@csrf_exempt
def get_reconnendUser(request):
    username = request.session['name']
    user = User.objects.get(username=username)
    reconnend_user= reconnendUser(user.userid)
    reconnend_users = []
    for recon in reconnend_user:
        reconnend_users.append([recon.book_name, str(recon.book_image), recon.book_id])
    return JsonResponse(reconnend_users, safe=False)


@csrf_exempt
def get_reconnendBook(request, n):
    reconnend_book = reconnendBook(n)
    reconnend_books = []
    for recon in reconnend_book:
        reconnend_books.append([recon.book_name, str(recon.book_image), recon.book_id])
    return JsonResponse(reconnend_books, safe=False)
