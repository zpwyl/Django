import re
import requests
from bs4 import BeautifulSoup


def get_cur_bookdata(url):
    html = requests.get(url)
    bsObj = BeautifulSoup(html.text, 'html.parser')
    #图书图片
    book_image = bsObj.select('div.pic > a.img > img')[0].get('src')
    #书名
    book_name = bsObj.select('div.name_info > h1')[0].get('title')
    #作者
    book_author = bsObj.select('span#author > a')[0].get_text()
    #IBSN
    book_IBSN = re.search(r'\d+', bsObj.select('ul.key > li')[4].get_text()).group()
    #价格
    book_price = re.search(r'\d+', bsObj.select('p#dd-price')[0].get_text()).group()
    # 出版社
    book_press = bsObj.select('span.t1')[1].get_text()
    #日期
    book_date = bsObj.select('span.t1')[2].get_text()
    #简介
    book_brief =  bsObj.select('div.name_info > h2 > span')[0].get('title')
    print(book_name)

def get_cur_url(url):
    # url = 'http://category.dangdang.com/cp01.54.00.00.00.00.html'
    html = requests.get(url)
    bsObj = BeautifulSoup(html.text, 'html.parser')
    #每一本书的链接
    urls = map(lambda x: bsObj.select('ul.bigimg > li > a')[x], range(0, 60))
    for ur in urls:
        u = ur.get('href')
        get_cur_bookdata(u)
    next_url = get_next_url(url)
    get_cur_url(next_url)


def get_next_url(url):
    html = requests.get(url)
    bsObj = BeautifulSoup(html.text, 'html.parser')
    next_url = 'http://category.dangdang.com' + bsObj.select('li.next > a')[0].get('href')
    if len(next_url)==0:
        print('没有下一页')
    else:
        return next_url


if __name__ == '__main__':
    url = 'http://category.dangdang.com/cp01.54.00.00.00.00.html'
    get_cur_url(url)