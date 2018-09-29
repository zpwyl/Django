import hashlib
import re
from datetime import datetime, timedelta
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter


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


def get_over_day(date):
    cday = datetime.strptime(date, '%Y-%m-%d')
    return cday


class get_yzm:
    def __init__(self, s, width, height):
        self.s = s
        self.width = width
        self.height = height

    # 随机字母:
    def rndChar(self, s):
        # s = ""
        n = random.randint(1, 2)  # n = 1  生成数字  n=2  生成字母
        if n == 1:
            numb = random.randint(0, 9)
            s += str(numb)
        else:
            nn = random.randint(1, 2)
            cc = random.randint(1, 26)
            if nn == 1:
                numb = chr(64 + cc)
                s += numb
            else:
                numb = chr(96 + cc)
                s += numb
        return s

    # 随机颜色1:
    def rndColor(self):
        return (random.randint(64, 255), random.randint(64, 255), random.randint(64, 255))

    # 随机颜色2:
    def rndColor2(self):
        return (random.randint(32, 127), random.randint(32, 127), random.randint(32, 127))

    def get_yzm(self):
        # 240 x 60:
        # width = 60 * 4
        # height = 60
        image = Image.new('RGB', (self.width, self.height), (255, 255, 255))
        # 创建Font对象:
        font = ImageFont.truetype('arial.ttf', 36)
        # 创建Draw对象:
        draw = ImageDraw.Draw(image)
        # 填充每个像素:
        for x in range(self.width):
            for y in range(self.height):
                draw.point((x, y), fill=get_yzm.rndColor(self))
        yzm = ''
        # 输出文字:
        for t in range(4):
            s = get_yzm.rndChar(self, '')
            draw.text((20 * t + 10, 2), s, font=font, fill=get_yzm.rndColor2(self))
            yzm += s

        # 模糊:
        image = image.filter(ImageFilter.BLUR)
        image.save('static/img/code.jpg', 'jpeg')
        return yzm







