import time
import os
from skimage import io
import numpy as np
import matplotlib.pyplot as plt
import csv
import pandas as pd

import copy_selected_plant_photos
import count_area
import prediction


def import_images(folder):
    '''
    Makes an iterable images list

    :param folder: path to a folder where to get photos
    :return: generator object of numpy.ndarray images
    '''
    assert os.path.exists(folder)
    images_path = [f for f in os.listdir(folder) if os.path.splitext(f)[1] == '.jpg']
    return ({'time': img[:-4], 'image': io.imread(os.path.join(folder, img))} for img in images_path)


def show_image(image):
    plt.imshow(image)
    plt.show()


def show_hist(h, line=None):
    plt.hist(h)
    if line is not None:
        plt.axvline(line, color='r')
    plt.show()


def show_plots(data):
    fig = plt.figure(figsize=(10, 10))
    for plant in range(len(data)):
        a = fig.add_subplot(len(data), 1, plant + 1)
        a.plot(data[plant])

    plt.show()

# Making dataset that consists of images of selected desks with plants
# copy_selected_plant('all_photos', 6)


# Importing images from dataset
# images = import_images('6_plant')


# Calculating areas of plants on the desk
# count_area.calculate_squares(images)


# Calculating areas of one selected plant on the desk
# count_area.calculate_single_plant(images, 2)


# Getting raw array with areas of one selected plant
# show_plots([count_area.read_areas_from_file(2, type='array')])


# Getting Pandas.Series with areas of one selected plant
areas = count_area.read_areas_from_file(2)
