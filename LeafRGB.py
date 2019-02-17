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


class LeafRGB:
    def __init__(self, img):
        self.rgb_image = img
        self.shape = img.shape
        self.count_green_and_red()
        self.count_squares()

    def count_green_and_red(self):
        ''' Counts green and red pixels on the rgb image. Creates green and red masks. '''
        green = 0
        red = 0

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

        green_mask = np.ndarray(self.shape)
        red_mask = np.ndarray(self.shape)

        for row in range(self.shape[0]):
            for col in range(self.shape[1]):
                if is_green(self.rgb_image[row, col]):
                    green_mask[row, col] = 1
                    green += 1
                if is_red(self.rgb_image[row, col]):
                    red_mask[row, col] = 1
                    red += 1

        self.green_mask = green_mask
        self.red_mask = red_mask
        self.red_pixels = red
        self.green_pixels = green

    def show_all(self):
        ''' Shows a plot consists of an image and its green and red masks
            Prints leaf square
        '''
        fig = plt.figure()
        fig.set_figheight(15)
        fig.set_figwidth(15)

        a = fig.add_subplot(1, 3, 1)
        imgplot = plt.imshow(self.rgb_image)
        a.set_title('Initial image')

        a = fig.add_subplot(1, 3, 2)
        imgplot = plt.imshow(self.green_mask)
        a.set_title('Green mask')

        a = fig.add_subplot(1, 3, 3)
        imgplot = plt.imshow(self.red_mask)
        a.set_title('Red mask')

        fig.show()

        print("leaf square is: " + str(round(self.green_square, 2)))

    def count_squares(self):
        ''' Counts leaf square '''
        self.pxl_square = 1 / self.red_pixels  # square centimeters
        self.green_square = self.green_pixels * self.pxl_square  # square centimeters

