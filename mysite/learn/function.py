# -*- coding: utf-8 -*-

"""
辅助功能：

"""

__author__ = 'zp'

from PIL import Image, ImageDraw, ImageFont, ImageFilter

import random

class function:
    def message(message):
        return {'message': message}

    def messages(num, messages):
        return {'num': num, 'messages': messages}


class get_yzm:
    # 随机字母:
    def rndChar():
        s = ""
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
    def rndColor():
        return (random.randint(64, 255), random.randint(64, 255), random.randint(64, 255))

    # 随机颜色2:
    def rndColor2():
        return (random.randint(32, 127), random.randint(32, 127), random.randint(32, 127))

    def get_yzm():
        # 240 x 60:
        width = 60 * 4
        height = 60
        image = Image.new('RGB', (width, height), (255, 255, 255))
        # 创建Font对象:
        font = ImageFont.truetype('arial.ttf', 36)
        # 创建Draw对象:
        draw = ImageDraw.Draw(image)
        # 填充每个像素:
        for x in range(width):
            for y in range(height):
                draw.point((x, y), fill=get_yzm.rndColor())
        yzm = ''
        # 输出文字:
        for t in range(4):
            s = get_yzm.rndChar()
            draw.text((60 * t + 10, 10), s, font=font, fill=get_yzm.rndColor2())
            yzm += s

        # 模糊:
        image = image.filter(ImageFilter.BLUR)
        image.save('./learn/templates/img/code.jpg', 'jpeg')
        return yzm

