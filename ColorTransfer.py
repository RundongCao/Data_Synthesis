import numpy as np
import cv2

import parsingJson
import os


def img_transfer(file_name, file_out):
    img = cv2.imread(file_name)
    b, g, r = cv2.split(img)

    grayImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, bi_mask = cv2.threshold(grayImg, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    _, bi_img = cv2.threshold(grayImg, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    new_img_b = cv2.bitwise_and(bi_img, b)
    new_img_g = cv2.bitwise_and(bi_img, g)
    new_img_r = cv2.bitwise_and(bi_img, r)

    new_img_b = cv2.bitwise_or(new_img_b, bi_mask)
    new_img_g = cv2.bitwise_or(new_img_g, bi_mask)
    new_img_r = cv2.bitwise_or(new_img_r, bi_mask)

    new_img = cv2.merge([new_img_b,new_img_g,new_img_r])
    cv2.imwrite('Colordataset/'+file_out, new_img)


if __name__ == '__main__':
    o_path = './Output/equal'

    for file in os.listdir(o_path):
            #print(file)
        file_name = o_path + '/' + file
        file_out = 'equal' + '/' + file
        img_transfer(file_name, file_out)
