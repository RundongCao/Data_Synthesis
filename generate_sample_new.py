# -*- coding:utf-8 -*-
import os
import random
import pygame
from random import choice

import numpy as np
import cv2

from PIL import Image, ImageDraw, ImageFont
import time

pygame.init()
global pixel_mean

global ft

dict = {'0':20,'1':1,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'+':10,'-':11,'×':12, '÷':13,'(':14, ')':15,'=':16, '>':17,'<':18,'rect':19,'[':25,']':26,'≤':27,'≈':23,'.':22}
dict_hanzi={'一':36,'三':38,'四':39,'五':40,'六':41,'七':42,'升':45,'只':46,'个':47,'里':48,'根':49,'张':50,'半':52,'棵':53,'元':54,'角':55,'分':56,'十':57,'百':58,
            '万':59,'亿':60,'千':61,'米':62,'毫':63,'厘':64,'立':65,'平':66,'方':67,'公':68,'顷':69,'吨':70,'克':71,'斤':72,'年':73,'月':74,'日':75,'天':76,'星':78,
            '期':79,'钟':80,'秒':81,'小':82,'时':83}
dict_zimu={'a':84,'A':85,'b':86,'B':87,'c':88,'C':89,'D':90,'d':91,'e':92,'E':93,'f':94,'F':95,'g':96,'G':97,'h':98,'H':99,'i':100,'I':101,'j':102,'J':103,'K':104,\
            'k':105,'l':106,'L':107,'m':108,'M':109,'n':110,'N':111,'o':112,'O':113,'p':114,'P':115,'Q':116,'q':117,'r':118,'R':119,'s':120,'S':121,'t':122,'T':123,\
            'u':124,'U':125,'v':126,'V':127,'w':128,'W':129,'x':130,'X':131,'y':132,'z':133,'Z':134}

dict_mean={'bkg\\6.jpg':243,'bkg\\1.jpg':222,'bkg\\2.jpg':228,'bkg\\7.jpg':221,'bkg\\5.jpg':226,'bkg\\3.jpg':231,'bkg\\8.jpg':187,'bkg\\4.jpg':230}

list_hanzi = ['一', '三', '四', '五', '六', '七', '升', '只', '个', '里', '根', '张', '半', '棵', '元', '角', '分', '十', '百', '万', '亿',
                '千', '米', '毫', '厘', '立', '平', '方','公', '顷', '吨', '克', '斤', '年', '月', '日', '天', '星', '期', '钟', '秒', '小', '时']
list_zimu =['a','b','c','C','d','g', 'h', 'i','K','k','L','m','n','o','s','S','t', 'v', 'x', 'y']

list_hanzi_1=['元','角','分']
list_hanzi_2=['亿','万']
list_hanzi_3=['千米','米','分米','厘米','毫米','公分']
list_hanzi_4=['平方千米','公顷','平方米','平方分米','平方厘米','平方毫米']
list_hanzi_5=['吨','千克','克','斤','公斤']
list_hanzi_6=['年','月','天','时','小时','周','分钟','分','秒','毫秒','日']
list_hanzi_7=['个']


color = (80, 80, 80)

# backgroud set
bkdir = 'bkg'
def get_bks(bkdir):
    bks = []
    list = os.listdir(bkdir)
    for i in range(len(list)):
        path = os.path.join(bkdir,list[i])
        if os.path.isfile(path) and path[-3:]=='jpg':
            bks.append(path)
    return bks

def get_bk():
    bl = len(bks)
    img = bks[random.randint(0, bl - 1)]
    global pixel_mean
    pixel_mean=dict_mean[img]
    #print("pixel_mean:",pixel_mean)
    return pygame.image.load(img)


#fonts = ["arial.ttf","arialbd.ttf","ARIALNBI.ttf","STFANGSO.ttf","times.ttf","BASKVILL.ttf","comic.ttf","SIMYOU.ttf","simsun.ttc","STHUPO.ttf","FZSTK.ttf","STENCIL.ttf","MISTRAL.ttf","FTLTLT.ttf","COOPBL.ttf","STSONG.ttf","simfang.ttf"]
fonts = ['simsun.ttc','STSONG.TTF','STFANGSO.TTF','simfang.ttf','simsunb.ttf','STKAITI.TTF','times.ttf']
#fonts_hanzi=['simsun.ttc','simfang.ttf','simhei.ttf']
fonts_hanzi=['simsun.ttc','STSONG.TTF','STFANGSO.TTF','simfang.ttf','simsunb.ttf','STKAITI.TTF','times.ttf']

def get_font(ftype,size):
    return pygame.font.Font(u'C:\\Windows\\Fonts\\'+ftype,size)

def get_font_zimu(ftype,size):
    return pygame.font.Font(ftype,size)

#尺寸变化[0.8,1.5]
def get_size(txt,scale):
    val = ft.size(txt)
    w = int(val[0]*scale)
    h = int(val[1]*scale)
    return [w,h]

# draw one text
def draw_one(txt,size,pose,color):
    sf = ft.render(txt,0,color)
    sf = pygame.transform.scale(sf,size)
    bk.blit(sf,pose)
    return (pose[0],pose[1],size[0],size[1])

def generate_approximate(name):
    #A opt B ≈ C
    scale = 1.0
    ops = [u'+', u'-', u'\u00D7', u'\u00F7']
    op = ops[random.randint(0, 3)]
    judge = '≈'  # 运算符

    A = str(random.randint(0, 9))
    B = str(random.randint(0, 9))
    C = str(random.randint(0, 9))

    sa = get_size(A,scale)  # w,h
    sb = get_size(B,scale)
    sc = get_size(C,scale)
    so = get_size(op,scale)
    sj = get_size(judge,scale)

    param = []  # 保存参数

    #现在要改成 A opt B ≈ C
    #A
    x=10
    y=10
    a_info = {"x": x, "y":y, "w": sa[0], "h":sa[1], "label":dict[A],"content":A}
    param.append(a_info)
    #opt
    mo = {"x": x+sa[0]+10, "y":y, "w": so[0],"h": so[1], "label": dict[op],"content":op}
    param.append(mo)
    #B
    b_info = {"x":x+sa[0]+10+so[0]+10, "y": y, "w": sb[0], "h": sb[1], "label":dict[B],"content":B}
    param.append(b_info)
    #≈
    sj_info = {"x":x+sa[0]+10+so[0]+10+sb[0]+10, "y": y, "w": sj[0], "h": sj[1], "label":23,"content":'≈'}
    param.append(sj_info)
    #C
    c_info = {"x": x + sa[0] + 10 + so[0] + 10 + sb[0] + 10+sj[0]+10, "y": y, "w": sc[0], "h": sc[1], "label": dict[C],"content":C}
    param.append(c_info)

    #rect尺寸固定
    rect = {"y": 0, "x": 0, "h":100, "w": 250, "label": dict["rect"], "content": "rect"}
    param.append(rect)
    tx = param #公式中各个字符的标签信息

    tuple = ((69,46,54),(21,14,8),(77,109,94),(59,44,51),(30,39,94),(145,143,148),(102,100,88),(155,152,146),(57,56,48),(93,83,86))
    tuple_index = random.randint(0,9)

    label = []
    i = tx[-1]
    w,h = bk.get_size()
    rw = random.randint(5,30)#随机数
    rh = random.randint(5,30)
    rw2 = random.randint(5,30)
    rh2 = random.randint(5,30)
    if w - i['w'] - i['x'] - 60 < 10:
        bw = random.randint(10,20)
        bh = random.randint(10,20)
    else:
        bw = random.randint(10,w-i['w']-i['x']-60)
        bh = random.randint(10,h-i['h']-i['y']-60)
    rect = (i['x']+bw,i['y']+bh,i['w']+rw+rw2,i['h']+rh+rh2)
    for i in tx[:-1]:
        iw = i['w']
        ih = i['h']
        ix = i['x']+bw+rw
        iy = i['y']+bh+rh
        draw_one(i['content'],(iw,ih),(ix,iy),tuple[tuple_index])
        label.append([name,i['x'], i['y'], i['x']+i['w'], i['y']+i['h'],i['label']])

    #提前判断rect是否已经超出图像的范围
    [w,h] = bk.get_size()
    if rect[0]+rect[2] > w or rect[1] + rect[3] > h:
        return 0
    else:
        pygame.image.save(bk.subsurface(rect), name)#resize之后再保存
        return label #

def generate_barcket(name):
    #[A opt B] = C
    scale = 1.0
    ops = [u'+', u'-', u'\u00D7', u'\u00F7']
    op = ops[random.randint(0, 3)]
    judge = '='  # 运算符

    A = str(random.randint(0, 9))
    B = str(random.randint(0, 9))
    C = str(random.randint(0, 9))

    sa = get_size(A,scale)  # w,h
    sb = get_size(B,scale)
    sc = get_size(C,scale)
    so = get_size(op,scale)
    sj = get_size(judge,scale)
    s_left = get_size('[',scale)
    s_right = get_size(']', scale)

    param = []  # 保存参数

    #[
    x = 10
    y = 10
    left_bracket = {"x": x, "y":y, "w": s_left[0], "h":s_left[1], "label":dict['['],"content":'['}
    param.append(left_bracket)
    #A
    a_info = {"x": left_bracket['x']+left_bracket['w']+10, "y":y, "w": sa[0], "h":sa[1], "label":dict[A],"content":A}
    param.append(a_info)
    #opt
    mo = {"x": a_info['x']+a_info['w']+10, "y":y, "w": so[0],"h": so[1], "label": dict[op],"content":op}
    param.append(mo)
    #B
    b_info = {"x":mo['x']+mo['w']+10, "y": y, "w": sb[0], "h": sb[1], "label":dict[B],"content":B}
    param.append(b_info)
    #]
    right_bracket = {"x": b_info['x']+ b_info['w'] + 10, "y": y, "w": s_right[0], "h": s_right[1], "label":dict[']'] , "content":']'}
    param.append(right_bracket)
    #=
    sj_info = {"x":right_bracket['x']+right_bracket['w']+10, "y": y, "w": sj[0], "h": sj[1], "label":16,"content":'='}
    param.append(sj_info)
    #C
    c_info = {"x": sj_info['w']+sj_info['x']+10, "y": y, "w": sc[0], "h": sc[1], "label":dict[B],"content":C}
    param.append(c_info)

    #rect尺寸固定
    rect = {"y": 0, "x": 0, "h":100, "w": 250, "label": dict["rect"], "content": "rect"}
    param.append(rect)
    tx = param #公式中各个字符的标签信息

    tuple = ((69,46,54),(21,14,8),(77,109,94),(59,44,51),(30,39,94),(145,143,148),(102,100,88),(155,152,146),(57,56,48),(93,83,86))
    tuple_index = random.randint(0,9)

    label = []
    i = tx[-1]
    w,h = bk.get_size()
    rw = random.randint(5,10)#随机数
    rh = random.randint(5,10)
    rw2 = random.randint(5,30)
    rh2 = random.randint(5,30)
    if w - i['w'] - i['x'] - 60 < 10:
        bw = random.randint(10,15)
        bh = random.randint(10,15)
    else:
        bw = random.randint(10,w-i['w']-i['x']-60)
        bh = random.randint(10,h-i['h']-i['y']-60)
    rect = (i['x']+bw,i['y']+bh,i['w']+rw+rw2,i['h']+rh+rh2)
    for i in tx[:-1]:
        iw = i['w']
        ih = i['h']
        ix = i['x']+bw+rw
        iy = i['y']+bh+rh
        draw_one(i['content'],(iw,ih),(ix,iy),tuple[tuple_index])
        label.append([name,i['x'], i['y'], i['x']+i['w'], i['y']+i['h'],i['label']])

    #提前判断rect是否已经超出图像的范围
    [w,h] = bk.get_size()
    if rect[0]+rect[2] > w or rect[1] + rect[3] > h:
        return 0
    else:
        pygame.image.save(bk.subsurface(rect), name)#resize之后再保存
        return label #

def generate_less_equal(name):
    #A opt B ≤ C
    scale = 1.0
    ops = [u'+', u'-', u'\u00D7', u'\u00F7']
    op = ops[random.randint(0, 3)]
    judge = '≤'  # 运算符

    A = str(random.randint(0, 9))
    B = str(random.randint(0, 9))
    C = str(random.randint(0, 9))

    sa = get_size(A,scale)  # w,h
    sb = get_size(B,scale)
    sc = get_size(C,scale)
    so = get_size(op,scale)
    sj = get_size(judge,scale)

    param = []  # 保存参数

    #现在要改成 A opt B ≈ C
    #A
    x=10
    y=10
    a_info = {"x": x, "y":y, "w": sa[0], "h":sa[1], "label":dict[A],"content":A}
    param.append(a_info)
    #opt
    mo = {"x": x+sa[0]+10, "y":y, "w": so[0],"h": so[1], "label": dict[op],"content":op}
    param.append(mo)
    #B
    b_info = {"x":x+sa[0]+10+so[0]+10, "y": y, "w": sb[0], "h": sb[1], "label":dict[B],"content":B}
    param.append(b_info)
    #≤
    sj_info = {"x":x+sa[0]+10+so[0]+10+sb[0]+10, "y": y, "w": sj[0], "h": sj[1], "label":27,"content":'≤'}
    param.append(sj_info)
    #C
    c_info = {"x": x + sa[0] + 10 + so[0] + 10 + sb[0] + 10+sj[0]+10, "y": y, "w": sc[0], "h": sc[1], "label":dict[C],"content":C}
    param.append(c_info)

    #rect尺寸固定
    rect = {"y": 0, "x": 0, "h":100, "w": 250, "label": dict["rect"], "content": "rect"}
    param.append(rect)
    tx = param #公式中各个字符的标签信息

    tuple = ((69,46,54),(21,14,8),(77,109,94),(59,44,51),(30,39,94),(145,143,148),(102,100,88),(155,152,146),(57,56,48),(93,83,86))
    tuple_index = random.randint(0,9)

    label = []
    i = tx[-1]
    w,h = bk.get_size()
    rw = random.randint(5,30)#随机数
    rh = random.randint(5,30)
    rw2 = random.randint(5,30)
    rh2 = random.randint(5,30)
    if w - i['w'] - i['x'] - 60 < 10:
        bw = random.randint(10,20)
        bh = random.randint(10,20)
    else:
        bw = random.randint(10,w-i['w']-i['x']-60)
        bh = random.randint(10,h-i['h']-i['y']-60)
    rect = (i['x']+bw,i['y']+bh,i['w']+rw+rw2,i['h']+rh+rh2)
    for i in tx[:-1]:
        iw = i['w']
        ih = i['h']
        ix = i['x']+bw+rw
        iy = i['y']+bh+rh
        draw_one(i['content'],(iw,ih),(ix,iy),tuple[tuple_index])
        label.append([name,i['x'], i['y'], i['x']+i['w'], i['y']+i['h'],i['label']])

    #提前判断rect是否已经超出图像的范围
    [w,h] = bk.get_size()
    if rect[0]+rect[2] > w or rect[1] + rect[3] > h:
        return 0
    else:
        pygame.image.save(bk.subsurface(rect), name)#resize之后再保存
        return label #



def generate_shuzi_zimu(name):
    #现在要改成 数字 字母 运算符 数字 字母  judge  [   ]  字母
    #             A   B     C     D    E      F     G  H   I
    scale = 1.0
    A = str(random.randint(0, 9))
    sa = get_size(A, scale)

    end=int(sa[0]*0.3)
    offset =random.randint(0, end)

    B = choice(list_zimu)
    sb = get_size(B, scale)

    ops = [u'+', u'-', u'\u00D7', u'\u00F7']
    C = ops[random.randint(0, 3)]
    sc = get_size(C, scale)

    D = str(random.randint(0, 9))
    sd = get_size(D, scale)

    E = choice(list_zimu)
    se = get_size(E, scale)

    judge=['=','<','>','≤','≈']
    F=choice(judge)
    sf = get_size(F, scale)
    if F=='≈':
        sf[0]=int(sf[0]*3/2)

    G='['
    sg = get_size(G, scale)
    H = ']'
    sh = get_size(H, scale)

    I = choice(list_zimu)
    si = get_size(I, scale)

    param = []  # 保存参数

    #现在要改成 数字 zimu 运算符 数字 zimu = ( ) zimu
    #             A   B     C     D    E   F G H  I
    # A
    x = 10
    y = 10
    a_info = {"x": x, "y": y, "w": sa[0], "h": sa[1], "label": dict[A], "content": A}
    param.append(a_info)
    # B
    b_info = {"x": x + sa[0] + offset, "y": y, "w": sb[0], "h": sb[1], "label":dict_zimu[B], "content": B}
    param.append(b_info)
    # C
    c_info = {"x": b_info['x'] + b_info['w'] + offset, "y": y, "w": sc[0], "h": sc[1], "label": dict[C], "content": C}
    param.append(c_info)
    #D
    d_info = {"x": c_info['x'] + c_info['w'] + offset, "y": y, "w": sd[0], "h": sd[1], "label":dict[D], "content": D}
    param.append(d_info)
    # E
    e_info = {"x": d_info['x'] + d_info['w'] + offset, "y": y, "w": se[0], "h": se[1], "label":dict_zimu[E], "content": E}
    param.append(e_info)
    # F
    f_info = {"x": e_info['x'] + e_info['w'] + offset, "y": y, "w": sf[0], "h": sf[1], "label": dict[F], "content":F}
    param.append(f_info)
    #G
    g_info = {"x": f_info['x']+f_info['w'] + offset, "y": y, "w": sg[0], "h": sg[1], "label":dict[G], "content": G}
    param.append(g_info)
    #H
    h_info = {"x": g_info['x'] + g_info['w'] + offset+25, "y": y, "w": sh[0], "h": sh[1], "label": dict[H], "content": H}
    param.append(h_info)
    #I
    i_info = {"x": h_info['x'] + h_info['w'] + offset, "y": y, "w": si[0], "h": si[1], "label": dict_zimu[I],"content": I}
    param.append(i_info)

    # rect尺寸固定
    rect = {"y": 0, "x": 0, "h": 90, "w": 380, "label": "rect", "content": "rect"}
    param.append(rect)
    tx = param  # 公式中各个字符的标签信息

    #tuple = ((69, 46, 54), (21, 14, 8), (77, 109, 94), (59, 44, 51), (30, 39, 94), (145, 143, 148), (102, 100, 88),
    #         (155, 152, 146), (57, 56, 48), (93, 83, 86))
    #tuple_index = random.randint(0, 9)
    global pixel_mean
    begin=pixel_mean//3
    end = pixel_mean//2
    pixel=random.randint(begin, end)
    tuple=(pixel, pixel, pixel)

    label = []
    i = tx[-1]
    w, h = bk.get_size()
    rw = random.randint(5, 30)  # 随机数
    rh = random.randint(5, 30)
    rw2 = random.randint(5, 30)
    rh2 = random.randint(5, 30)
    if w - i['w'] - i['x'] - 60 < 10:
        bw = random.randint(10, 20)
        bh = random.randint(10, 20)
    else:
        bw = random.randint(10, w - i['w'] - i['x'] - 60)
        bh = random.randint(10, h - i['h'] - i['y'] - 60)
    rect = (i['x'] + bw, i['y'] + bh, i['w'] + rw + rw2, i['h'] + rh + rh2)
    for i in tx[:-1]:
        iw = i['w']
        ih = i['h']
        ix = i['x'] + bw + rw
        iy = i['y'] + bh + rh
        if ('a'<=i['content'] and 'z'>=i['content']) or ('A'<=i['content'] and 'Z'>=i['content']):
            print('zimu:',i['content'])
            draw_one(i['content'], (iw, ih), (ix, iy), tuple)
        else:
            print('non_zimu:',i['content'])
            font_non_zimu = 'simfang.ttf'
            ft = get_font(font_non_zimu, 50)
            #draw_one(i['content'], (iw, ih), (ix, iy), tuple)
            txt=i['content']
            size=(iw, ih)
            pose=(ix, iy)
            color=tuple

            sf = ft.render(txt, 0, color)
            sf = pygame.transform.scale(sf, size)
            bk.blit(sf, pose)
            #return (pose[0], pose[1], size[0], size[1])

            #重置字体
            #font_zimu = 'timesi.ttf'
            #ft = get_font_zimu(font_zimu, 50)
        label.append([name, i['x'], i['y'], i['x'] + i['w'], i['y'] + i['h'], i['label']])

    # 提前判断rect是否已经超出图像的范围
    [w, h] = bk.get_size()
    if rect[0] + rect[2] > w or rect[1] + rect[3] > h:
        return 0
    else:
        a=pygame.image.tostring(bk.subsurface(rect), 'RGB')
        #print(type(a))
        b=bk.subsurface(rect).get_size()
        #print(b)
        pygame.image.save(bk.subsurface(rect), name)  # resize之后再保存
        return label

def generate_shuzi_hanzi_new(name1, name2):
    name = name1 + name2
    #现在要改成 数字 运算符 (数字)  = 数字
    #             A   B     C  D E  F  G
    scale = 1.0
    A = str(random.randint(0, 9))
    sa = get_size(A, scale)

    end=int(sa[0]*0.3)
    offset =random.randint(0, end)

    # B = choice(list_hanzi_7)
    # sb = get_size(B, scale)

    ops = [u'+', u'-', u'\u00D7', u'\u00F7']
    operator = random.randint(0, 3)
    B = ops[operator]
    sb = get_size(B, scale)

    C = '('
    sc = get_size(C, scale)

    D = str(random.randint(1, 99)/10)
    sd = get_size(D, scale)

    E = ')'
    se = get_size(E, scale)

    F = '='
    sf = get_size(F, scale)

    #G = str(random.randint(0, 9) / 10 + random.randint(0, 9))
    if operator == 0:
        G = str(format(int(A) + float(D),'.1f'))
    elif operator == 1:
        G = str(format(int(A) - float(D),'.1f'))
    elif operator == 2:
        G = str(format(int(A) * float(D),'.1f'))
    elif operator == 3:
        G = str(format(int(A) / float(D),'.1f'))

    sg = get_size(G, scale)


    HW = []
    param = []  # 保存参数

    #现在要改成 数字 汉字 运算符 数字 汉字 = ( ) 汉字
    #             A   B     C     D    E   F G H  I
    # A
    x = 10
    y = 5
    a_info = {"x": x, "y": y, "w": sa[0], "h": sa[1], "content": A}
    param.append(a_info)
    # B
    b_info = {"x": x + sa[0] + offset, "y": y, "w": sb[0], "h": sb[1], "content": B}
    param.append(b_info)
    # C
    c_info = {"x": b_info['x'] + b_info['w'] + offset, "y": y, "w": sc[0], "h": sc[1], "content": C}
    param.append(c_info)

    #D
    d_info = {"x": c_info['x'] + c_info['w'] + offset, "y": y, "w": sd[0], "h": sd[1], "content": D}
#    param.append(d_info)
    d1_info = {"x": c_info['x'] + c_info['w'] + offset , "y": y , "w": int(sd[0]/3), "h": sd[1], "content": D[0]}
    d2_info = {"x": c_info['x'] + c_info['w'] + offset + int(sd[0]/3), "y": y + 5*int(sd[1]/6), "w": int(sd[0]/7), "h": int(sd[1]/6), "content": 'point'}
    d3_info = {"x": c_info['x'] + c_info['w'] + offset + 2*int(sd[0]/3), "y": y, "w": int(sd[0]/3), "h": sd[1], "content": D[2]}
    HW.append(d1_info)
    HW.append(d2_info)
    HW.append(d3_info)

    # E
    e_info = {"x": d_info['x'] + d_info['w'] + offset, "y": y, "w": se[0], "h": se[1], "content": E}
    param.append(e_info)
    # F
    f_info = {"x": e_info['x'] + e_info['w'] + offset, "y": y, "w": sf[0], "h": sf[1], "content":F}
    param.append(f_info)
    #G
    g_info = {"x": f_info['x']+f_info['w'] + offset, "y": y, "w": sg[0], "h": sg[1],  "content": G}
    param.append(g_info)

    latex = name2 + ' ' + a_info["content"] + b_info["content"] + c_info["content"] + d_info["content"] + e_info["content"] + f_info["content"] + g_info["content"]

    # rect尺寸固定
    '''
     h_max = sa[1]
    if h_max < sb[1]:
        h_max = sb[1]
    if h_max < sc[1]:
        h_max = sc[1]
    if h_max < sd[1]:
        h_max = sd[1]
    if h_max < se[1]:
        h_max = se[1]
    if h_max < sf[1]:
        h_max = sf[1]
    if h_max < sg[1]:
        h_max = sg[1]
    '''

    h_max = 75

    width = x + sa[0] + sb[0] + sc[0] + sd[0] + se[0] + sf[0] + sg[0] + offset*6 + random.randint(2, 10)

    rect = {"y": 0, "x": 0, "h": h_max + 5, "w": width, "label": "rect", "content": "rect"}
    param.append(rect)
    tx = param  # 公式中各个字符的标签信息

    #tuple = ((69, 46, 54), (21, 14, 8), (77, 109, 94), (59, 44, 51), (30, 39, 94), (145, 143, 148), (102, 100, 88),
    #         (155, 152, 146), (57, 56, 48), (93, 83, 86))
    #tuple_index = random.randint(0, 9)
    global pixel_mean
    begin=pixel_mean//3
    end = pixel_mean//2
    pixel=random.randint(begin, end)
    tuple=(pixel, pixel, pixel)

    label = []

    i = tx[-1]
    w, h = bk.get_size()
    rw = random.randint(5, 30)  # 随机数
    rh = random.randint(5, 30)
    rw2 = random.randint(5, 30)
    rh2 = random.randint(5, 30)
    if w - i['w'] - i['x'] - 60 < 10:
        bw = random.randint(10, 20)
        bh = random.randint(10, 20)
    else:
        bw = random.randint(10, w - i['w'] - i['x'] - 60)
        bh = random.randint(10, h - i['h'] - i['y'] - 60)
    rect = (i['x'] + bw, i['y'] + bh, i['w'] + rw + rw2, i['h'] + rh + rh2)
    #print ("y is {}".format(i['y']))
    #print (bh)
    #print ("h is {}".format(i['h']))
    y_out = i['y'] + bh

    for i in tx[:-1]:
        iw = i['w']
        ih = i['h']
        ix = i['x'] + bw + rw
        iy = i['y'] + bh + rh
        draw_one(i['content'], (iw, ih), (ix, iy), tuple)
        label.append([name, i['x'], i['y'], i['x'] + i['w'], i['y'] + i['h']])


    # 提前判断rect是否已经超出图像的范围
    [w, h] = bk.get_size()
    if rect[0] + rect[2] > w or rect[1] + rect[3] > h:
        return 0
    else:
        a=pygame.image.tostring(bk.subsurface(rect), 'RGB')
        #print(type(a))
        b=bk.subsurface(rect).get_size()
        #print(b)
        pygame.image.save(bk.subsurface(rect), name)  # resize之后再保存
        return label, HW, y_out, latex

f = open('label.txt','a') #写入坐标信息
index = 0 #index代表样本数量
while index < 5000:
    print(index)
    index +=1
    bks = get_bks(bkdir)
    #num = random.randint(0, 2)
    #font_zimu='timesi.ttf'
    #ft = get_font_zimu(font_zimu, 50)

    font_non_zimu = 'simfang.ttf'
    ft = get_font(font_non_zimu, 50)

    path = ''
    labels = []
    bk = get_bk()
    img_dir=".//img//"
    save_dir = "./results/"
    data, HWs, y_out, latex = generate_shuzi_hanzi_new(img_dir , str(index) + ".png")

    #print (data)
    #print (np.shape(data))

    #im = Image.open(img_dir + str(index) + ".png")
    im = cv2.imread(img_dir + str(index) + ".png")
    #print (data)
    widthmax = []
    for hw in HWs:
        idc = "./Cutdataset/" + hw['content'] + "/"
        filename_list = os.listdir(idc)
        fileidx = random.randint(0, len(filename_list) - 1)
        filename = filename_list[fileidx]

        #img = Image.open(idc + filename)
        img = cv2.imread(idc + filename)

        img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
        #im = cv2.cvtColor(im, cv2.COLOR_BGR2BGRA)

        #print (im[0][0])
        '''
        for item in datas:
            if item[0] >= 245 and item[1] >= 245 and item[2] >= 245:
                newData.append((255, 255, 255, 0))
            else:
                newData.append(item)
        img.putdata(newData)
        '''

        # img.thumbnail([2 * hw['h'], 2 * hw['w']], Image.ANTIALIAS)

        dim = (int(hw['w']), int(hw['h']))
        #print (dim)
        img = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)

        imgh, imgw, c = np.shape(img)
        #print (np.shape(img) )

        for py in range(0, imgh):
            for px in range(0, imgw):
                if img[py][px][0] >= 245 and img[py][px][1] >= 245 and img[py][px][2] >= 245:
                    img[py][px][3] = 0
                    #print (img[py][px])

        #[imgw, imgh] = img.size

        print (hw['content'])
        print (y_out)
        #print (np.shape(img))
        #print (np.shape(im))
        if hw['content'] is "point":
            #im.paste(img, (int(hw['x'] + hw['w'] + 10), int(hw['y'] + 15 + hw['h'] / 2)), img)
            wd = int(hw['x'] + 15)
            hd = int(hw['y'] + 15)
            #print (hd)
            for py in range(hd, hd+imgh):
                for px in range(wd, wd+imgw):
                    if img[py-hd][px-wd][3]!=0:
                        im[py, px] = img[py - hd][px - wd][0:3]

            #im[hd:hd+imgh, wd:wd+imgw] = img
        else:
            #im.paste(img, (int(hw['x'] + hw['w'] + 10), int(hw['y'] + 15 )), img)
            wd = int(hw['x'] + 15)
            hd = int(hw['y'] + 15)
            #print (hd)
            for py in range(hd, hd+imgh):
                for px in range(wd, wd+imgw):
                    if img[py-hd][px-wd][3]!=0:
                        im[py, px] = img[py - hd][px - wd][0:3]
            #im[hd:hd+imgh, wd:wd+imgw] = img

        #imgw += int(hw['x'] + hw['w'] );
        #imgh += int(hw['y'] )
        #widthmax.append(int(hw['x'] + hw['w']) + img.size[0])

    #width = im.size[0]
    #height = im.size[1]
    #im = im.crop((0, 0, max(max(widthmax) , width), height))
    cv2.imwrite(save_dir + str(index) + '.png', im)
    #im.save(save_dir + str(index) + '.png')


    labels += latex + '\n'
    lines = labels
    #for i in labels:
    #    l = i
        #for j in i:
        #    l += str(j) + ' '
     #   l += '\n'
     #   lines.append(l)
    f.writelines(lines)
f.close()











