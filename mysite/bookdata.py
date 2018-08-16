import sqlite3
import requests
from bs4 import BeautifulSoup
import re
import time
import random

conn = sqlite3.connect('db.sqlite3')
c = conn.cursor()




def get_cur_html(url):
    html = requests.get(url)
    bsObj = BeautifulSoup(html.text, "lxml")
    time.sleep(random.randint(2, 5))
    #书名
    book_names = bsObj.findAll('a', {'name': 'itemlist-title'})

    for bookname in book_names:
        books_name = c.execute("""
            select book_name from learn_book 
        """)
        try:
            a = bookname.get('title')
            book_name = re.split(r'[\(\（\s\・\！\：]+', a)[1]
        except:
            continue
        else:
            if book_name in books_name:
                continue
            book_type = '文学'
            price = random.randint(30, 100)
            sql = """
            INSERT INTO learn_book(book_name , book_type , book_price) VALUES (? , ? , ? )
            """
            c.execute(sql, (book_name, book_type, price))
            conn.commit()
    get_next_html(url)


def get_next_html(url):
    html = requests.get(url)
    bsObj = BeautifulSoup(html.text, "lxml")
    pageHtml = bsObj.select('li.next > a')
    if len(pageHtml) == 0:
        print("已经没有下一页！")
        conn.close()
    else:
        global n
        n += 1
        print('--------第', n, '页------')
        next_page = 'http://search.dangdang.com' + pageHtml[0].get('href')
        get_cur_html(next_page)

if __name__ == '__main__':
    n = 0
    url = 'http://search.dangdang.com/?key=%CE%C4%D1%A7&act=input'
    get_cur_html(url)

