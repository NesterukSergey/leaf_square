import os
from skimage import io
from skimage.color import rgb2hsv
from skimage.filters import threshold_otsu
from skimage.filters.rank import median
from skimage.morphology import disk
import matplotlib.pyplot as plt
import cv2
import csv
import pandas as pd
import itertools


def is_blurred(img):
    '''
    Detects if the image is blurred

    :param img: np.ndarray
    :return: boolean, True if blurred
    '''
    variance = cv2.Laplacian(img, cv2.CV_64F).var()
    return variance < 40


def remove_blurred(areas, images):
    '''
    Replaces area value of blurred images with average of its neighbors

    :param areas: array of (7) arrays for every plant. Each contains areas measurements
    :param images: generator object
    :return: areas
    '''
    areas_to_remove = []
    desk_number = 0
    for desk in images:
        if is_blurred(desk['image']):
            areas_to_remove.append(desk_number)

        desk_number += 1

    for plant in range(len(areas)):
        for area in list(reversed(sorted(areas_to_remove))):
            if area == 0 or area == (len(areas[plant]) - 1):
                del areas[plant][area]
            else:
                areas[plant][area]['area'] = (areas[plant][area - 1]['area'] + areas[plant][area + 1]['area']) / 2

    return areas


def split_into_9_parts(image):
    '''
    Splits image into 9 parts
    |0|1|2|
    |3|4|5|
    |6|7|8|

    :param image: numpy.ndarray
    :return: list of 9 numpy.ndarrays
    '''
    vert = image.shape[0] // 3
    hor = image.shape[1] // 3
    ls = []

    for col in range(3):
        for row in range(3):
            ls.append(image[vert * col: vert * (col + 1),
                      hor * row: hor * (row + 1)])

    return ls


def count_green_pixels(img):
    '''
    Counts pixels in the image with high saturation using Otsu threshold
    Asserts that image background if white!

    :param img: np.ndarray
    :return: int
    '''
    hsv_image = rgb2hsv(img)
    saturation = hsv_image[:, :, 1]
    threshold = threshold_otsu(saturation)
    saturation = saturation > threshold * 1.3
    saturation = median(saturation, disk(2))  # filtering

    # show_image(saturation)
    pixels_count = saturation.mean() * saturation.shape[0] * saturation.shape[1] / saturation.max()
    return pixels_count


def count_pixel_square(img):
    '''
    :param img: ndarray, - image with 2 reference squares
    :return: one pixel square (cm^2)
    '''
    one_square = count_green_pixels(img) // 2
    return 1 / one_square


def write_areas_to_file(array, plant_number):
    '''
    Writes plant area series to [plant_number].csv file

    :param array: array of areas
    :param plant_number:
    :return: filename
    '''
    file = str(plant_number) + '_plant_areas.csv'
    with open(file, 'w', newline='') as csvfile:
        time = ['time']
        area = ['area']
        for measurement in range(len(array)):
            time.append(array[measurement]['time'])
            area.append(array[measurement]['area'])
        rows = zip(time, area)

        writer = csv.writer(csvfile)
        for row in rows:
            writer.writerow(row)

    return file


def read_areas_from_file(plant_number, type='pandas_series'):
    file = str(plant_number) + '_plant_areas.csv'

    if type == 'array':
        areas_array = []
        with open(file, newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                areas_array.append(row[1])

        areas_array.pop(0)
        return [float(s) for s in areas_array]

    # return pd.read_csv(file, header=0)
    return pd.Series.from_csv(file, header=0)


def calculate_squares(images, write_to_file=True):
    '''
    Adds calculated squares of plants' leafs from the desk to the storage
    |0|1|2|
    |3| | |
    |4|5|6| i.e. excluding reference square and empty part

    :param images: generator object, series of images of a desk with plants
    :param write_to_file: boolean, if True data would be written to file
    :return: array of areas
    '''
    init_images, images = itertools.tee(images)
    plants_growth = [[] for i in range(7)]
    for desk in images:
        parts = split_into_9_parts(desk['image'])
        pixels_count = []
        pixel_square = count_pixel_square(parts[4])

        for n in range(9):
            if (n == 4) or (n == 5):  # skipping reference square and empty part
                continue

            pixels_count.append(count_green_pixels(parts[n]))

        squares = [c * pixel_square for c in pixels_count]

        for plant in range(len(squares)):
            plants_growth[plant].append({
                'time': desk['time'],
                'area': squares[plant]
            })

    plants_growth = remove_blurred(plants_growth, init_images)

    if write_to_file:
        for plant in range(len(plants_growth)):
            write_areas_to_file(plants_growth[plant], plant)

    return plants_growth


def calculate_single_plant(images, plant_number, write_to_file=True):
    '''
    Calculates square of plants' leafs from one of the desks' parts[0...3, 6..8]

    :param images: generator object, series of one desk images
    :param plant_number:
    :param write_to_file: boolean, if True data would be written to file
    :return: series of plants' area
    '''
    area_series = []
    for desk in images:
        parts = split_into_9_parts(desk['image'])
        pixel_square = count_pixel_square(parts[4])
        # area_series.append(count_green_pixels(parts[plant_number]) * pixel_square)

        area_series.append({
            'time': desk['time'],
            'area': (count_green_pixels(parts[plant_number]) * pixel_square)
        })
    if write_to_file:
        write_areas_to_file(area_series, plant_number)

    return area_series
