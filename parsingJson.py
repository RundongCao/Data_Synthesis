#/usr/bin/env
# -*- coding:utf-8 -*-
import os
import json

def parse_box(box_text):
    x_ = box_text["left"]
    y_ = box_text["top"]
    width = box_text["width"]
    height = box_text["height"]
    return [x_, y_, width, height]

def parsingJsons(jpath):
    Exes = []
    latexes = []
    picNames = []
    oriExes = []
    BRecs = []
    for file in os.listdir(jpath):
        if file[-4:] != 'json':
            continue
        with open(os.path.join(jpath, file), 'r', encoding='utf-8') as load_f:
            for line in load_f.readlines():
                load_dict = json.loads(line)
                keys = list(load_dict.keys())
                pictureurl = keys[0]

                no = 0
                for d in load_dict[keys[0]]:
                    if d.__contains__('latex_check') and d['latex_check'] != 1:
                        print('skip latex_check failed:', d['latex_check'], pictureurl)
#                        count = count + 1
                        continue
                    tmpEx = []
                    tmpOriEx = []
                    boxes = d['extras']
                    try:
                        text_proc = d['text_process']
                    except:
                        text_proc = d['text']
                    lat = text_proc[text_proc.find('\\(')+2:text_proc.find('\\)')].replace('……', '...').replace('…', '...').replace(' ', '').replace('\\\\', '\\')
                    for i in range(len(boxes)):
                        if boxes[i]['desc'] == '公式' or boxes[i]['desc'] == '划线删除':
                            continue
                        box = parse_box(boxes[i]['box'])
                        box.append(1.0)
                        cl = boxes[i]['content_list'][0]
                        cl = charTrans(cl)
                        box.append(cl)
                        tmpOriEx.append(box)
                        tmpEx.append(box)

                    latexes.append(lat)
                    if 'https' in pictureurl:
                        #picNames.append(pictureurl.split('/')[-1][:-4]+'_'+str(no)+'.jpg')
                        picNames.append(pictureurl.split('/')[-1][:-4] +  '.jpg')
                    else:
                        #picNames.append(pictureurl[:-4]+'_'+str(no)+'.jpg')
                        picNames.append(pictureurl[:-4] +  '.jpg')
                    no += 1
                    BRecs.append(parse_box(d['box']))
                    Exes.append(tmpEx)
                    oriExes.append(tmpOriEx)
                    # latexes.append(tmpLat)
    return Exes, latexes, picNames, oriExes, BRecs


def charTrans(char):
    char = char.replace(' ', '')
    if (char == u"1" or char == u"□1"):
        label = '1'
    elif (char == u"2" or char == u"□2" or char == '²'):
        label = '2'
    elif (char == u"3" or char == u"□3" or char == '³'):
        label = '3'
    elif (char == u"4" or char == u"□4"):
        label = '4'
    elif (char == u"5" or char == u"□5"):
        label = '5'
    elif (char == u"6" or char == u"□6"):
        label = '6'
    elif (char == u"7" or char == u"□7"):
        label = '7'
    elif (char == u"8" or char == u"□8"):
        label = '8'
    elif (char == u"9" or char == u"□9"):
        label = '9'
    elif (char == u"0" or char == u"□0"):
        label = '0'
    elif (char == u"=" or char == u"＝" or char == u"\\(=\\)" or char == u"○=" or char == u"○＝"):
        label = '='
    elif (char == u"+" or char == u"＋" or char == "+" or char == u"\\(+\\)" or char == u"○+" or char == '□+'):
        label = '+'
    elif (char == u"-" or char == u"－" or char == "-" or char == u"\\(-\\)" or char == u"○-" or char == '□-'):
        label = '-'
    elif (char == u"×" or char == u"\\(\\times\\)" or char == u"○×" or char == '*'):
        label = '\\times'
    elif (char == u"÷" or char == u"÷" or char == u"\\(\\div \\)" or char == u"○÷" or char == '\\(\\div\\)'):
        label = '\\div'
    elif (char == u">" or char == u"＞" or char == u"○>" or char == u"○＞"):  # or ex["content_list"][-1]==u">"):
        label = '>'
    elif (char == u"<" or char == u"＜" or char == u"○<" or char == u"○＜"):  # or ex["content_list"][-1]==u"<"):
        label = '<'
    elif (char == u"(" or char == '﹙' or char == '（'):
        label = '('
    elif (char == u")" or char == '）' or char == '﹚'):
        label = ')'
    elif char == '{':
        label = '{'
    elif char == '}':
        label = '}'
    elif (char == u"/"):
        label = '\\'
    elif (char == u"……" or char == u"......" or char == u"..." or char == u"…" or char == '.....'):
        label = '...'
    elif (char == u"."):
        label = '.'
    elif (char == u"≈" or char == '\\(\\approx\\)'):
        label = '\\approx'
    elif char == '%' or char == '\\%':
        label = '\\%'
    elif char == '°' or char == '^{\\circ}':
        label = '^{\\circ}'
    else:
        return char
    return label


if __name__ == '__main__':
    # exr:小框 x,y,w,h,prec,char lat:latex 公式, picN:图像名
    exr, lat, picN, oriR, oriBRs = parsingJsons('./new_json_7k_fix')
    print('done')