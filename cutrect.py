import numpy as np
import cv2
import matplotlib.pyplot as plt
import parsingJson
import os


def img_transfer(file_name, file_out):
    img = cv2.imread(file_name)
    b, g, r = cv2.split(img)

    grayImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, bi_mask = cv2.threshold(grayImg, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    _, contours, _ = cv2.findContours(bi_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    mask = np.zeros_like(grayImg)  # Create mask where white is what we want, black otherwise
    cv2.drawContours(mask, contours, -1, 255, -1)  # Draw filled contour in mask

    #print(mask)


    # Now crop
    (x, y) = np.where(mask == 255)
    (topx, topy) = (np.min(x), np.min(y))
    (bottomx, bottomy) = (np.max(x), np.max(y))

    outb = np.ones_like(b)  # Extract out the object and place into output image
    outb = outb * 255

    outb[mask == 255] = b[mask == 255]
    outb = outb[topx:bottomx + 1, topy:bottomy + 1]



    outg = np.ones_like(g)  # Extract out the object and place into output image
    outg = outg * 255

    outg[mask == 255] = g[mask == 255]
    outg = outg[topx:bottomx + 1, topy:bottomy + 1]

    outr = np.ones_like(r)  # Extract out the object and place into output image
    outr = outr * 255

    outr[mask == 255] = r[mask == 255]
    outr = outr[topx:bottomx + 1, topy:bottomy + 1]

    new_img = cv2.merge([outb, outg, outr])



    cv2.imwrite('Cutdataset/'+file_out, new_img)


if __name__ == '__main__':
    o_path = './Colordataset'

    for dirs in os.listdir(o_path):
        print(dirs)
        dir_name = o_path + '/' + dirs
        for file in os.listdir(dir_name):
            #print(file)
            file_name = dir_name + '/' + file
            file_out = dirs + '/' + file
            img_transfer(file_name, file_out)

