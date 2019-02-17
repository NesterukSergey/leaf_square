'''
This script counts approximate square of leafs on a photo 

Assumes:
red reference square on right top is 1cm^2
path to photos from script is "testDataset/*filename*.jpg"
'''

import numpy as np
import os
from skimage import io
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

import time


def is_green(pxl):
    '''
    Assume that pixel is green if:
    red channel is < 225 (out of 255)
    green channel is > 100 (out of 255)
    blue channel is < 160 (out of 255)
    and blue channel < red channel < green channel

    Args:
    pxl (list): [r, g, b] values in [0-255]

    Returns:
    bool: True if pixel is green

    '''
    return np.all([(int(pxl[0]) < 225),
                   (int(pxl[1]) > 100),
                   (int(pxl[2]) < 160),
                   (int(pxl[0]) - int(pxl[2]) > 10),
                   (int(pxl[1]) - int(pxl[0]) > 5)])


def is_red(pxl):
    '''
    Assume that pixel is red if:
    red channel is > 100 (out of 255)
    and blue channel <= green channel < red channel

    Args:
    pxl (list): [r, g, b] values in [0-255]

    Returns:
    bool: True if pixel is red
    '''
    return np.all([(int(pxl[0]) > 100),
                   (int(pxl[0]) - int(pxl[1]) > 15),
                   (int(pxl[0]) - int(pxl[2]) > 15)])


def green_mask(img):
    '''
    Making a green mask to compare with leaf shape

    Args:
    img (np.ndarray): image

    Returns:
    mask (np.ndarray): image with white pixels on places of green pixels on initial image

    '''
    mask = np.ndarray(img.shape)

    for row in range(img.shape[0]):
        for col in range(img.shape[1]):
            mask[row, col] = 1 if is_green(img[row, col]) else 0

    return mask


def red_mask(img):
    '''
    Making a red mask to compare with reference square shape

    Args:
    img (np.ndarray): image

    Returns:
    mask (np.ndarray): image with white pixels on places of red pixels on initial image
    '''
    mask = np.ndarray(img.shape)

    for row in range(img.shape[0]):
        for col in range(img.shape[1]):
            mask[row, col] = 1 if is_red(img[row, col]) else 0

    return mask


def create_masks(img_list):
    '''
    Creates a list of images with their masks

    Args:
    img_list (list of numpy.ndarrays): the list of images

    Returns:
    list (list of objects) formated as
        {
        'img': numpy.ndarray,
        'g_mask': numpy.ndarray,
        'r_mask': numpy.ndarray
        }
    '''
    list = [{'img': i, 'g_mask': green_mask(i), 'r_mask': red_mask(i)} for i in img_list]
    return list


def count_pxls(mask):
    '''
    Counts white pixels in image (mask)

    Args:
    mask (numpy.ndarray): image (mask)

    Returns:
    count (int): count of white pixels
    '''
    count = 0
    for row in range(mask.shape[0]):
        for col in range(mask.shape[1]):
            if int(mask[row][col][0] == 1):
                count += 1

    return count


def show_mask(img_with_mask):
    '''
    Shows a plot consists of an image and its green and red masks

    Args:
    img_with_mask(list of objects): list of images wits masks
    '''
    fig = plt.figure()
    fig.set_figheight(15)
    fig.set_figwidth(15)

    a = fig.add_subplot(1, 3, 1)
    imgplot = plt.imshow(img_with_mask['img'])
    a.set_title('Initial image')

    a = fig.add_subplot(1, 3, 2)
    imgplot = plt.imshow(img_with_mask['g_mask'])
    a.set_title('Green mask')

    a = fig.add_subplot(1, 3, 3)
    imgplot = plt.imshow(img_with_mask['r_mask'])
    a.set_title('Red mask')

    fig.show()


def show_img_info(image_with_masks):
    '''
    Shows images as plots and prints information about calculated squares

    Args:
    img_with_mask(list of objects): list of images wits masks

    Returns:
    green_square (float): square of leafs in cm^2
    '''
    red_pxls = count_pxls(image_with_masks['r_mask'])
    green_pxls = count_pxls(image_with_masks['g_mask'])

    '''
    calculate the area of one pixel
    based on assumption that reference red square is 1 cm^2
    '''
    pxl_square = 1 / red_pxls  # square centimeters

    green_square = green_pxls * pxl_square  # square centimeters

    print("Leaf square: " + str(round(green_square, 2)) + " cm^2")
    print("Red pixels: " + str(round(red_pxls, 2)))
    print("Green pixels: " + str(round(green_pxls, 2)))
    print()

    show_mask(image_with_masks)
    return green_square
