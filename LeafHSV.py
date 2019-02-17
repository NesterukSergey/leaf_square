import numpy as np
import matplotlib.pyplot as plt
from skimage.color import rgb2hsv


class LeafHSV:
    '''
    This class counts approximate square of leafs on a photo

    Assumes:
    red reference square on right top is 1cm^2
    '''

    def __init__(self, img):
        self.rgb_image = img
        self.hsv_image = rgb2hsv(self.rgb_image)
        # self.hue_image = self.hsv_image[:, :, 0]
        self.shape = img.shape
        # self.value_image = self.hsv_image[:, :, 2]
        self.count_green_and_red()
        self.count_squares()

    def count_green_and_red(self):
        ''' Counts green and red pixels on the hsv image. Creates green and red masks. '''
        green = 0
        red = 0

        def is_green(pxl):
            '''
            Args:
            pxl (list): [h, s, v] values in [0-1]

            Returns:
            bool: True if pixel is green
            '''
            return np.all([(60 / 360 < pxl[0] < 200 / 360),
                           (pxl[1] > 0.25)
                           ])

        def is_red(pxl):
            '''
            Args:
            pxl (list): [h, s, v] values in [0-1]

            Returns:
            bool: True if pixel is red
            '''
            # print(pxl)
            return np.all([(300/360 < pxl[0] < 360/360),
                           (pxl[1] > 0.3)
                           ])

        green_mask = np.ndarray(self.shape)
        red_mask = np.ndarray(self.shape)

        for row in range(self.shape[0]):
            for col in range(self.shape[1]):
                if is_green(self.hsv_image[row, col]):
                    green_mask[row, col] = 1
                    green += 1
                if is_red(self.hsv_image[row, col]):
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
