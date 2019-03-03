import time
import os
from skimage import io
from skimage.color import rgb2hsv
from skimage.filters import threshold_otsu
from skimage.filters.rank import median
from skimage.morphology import disk
import numpy as np
import matplotlib.pyplot as plt


def import_images(folder):
    '''
    Makes an iterable images list

    :param folder: path to a folder where to get photos
    :return: generator object of numpy.ndarray images
    '''
    assert os.path.exists(folder)

    images_path = [f for f in os.listdir(folder) if os.path.splitext(f)[1] == '.jpg']

    return (io.imread(os.path.join(folder, img)) for img in images_path)


def show_image(image):
    ip = plt.imshow(image)
    plt.show()


def show_hist(h, line=None):
    plt.hist(h)
    if not line is None:
        plt.axvline(line, color='r')
    plt.show()


def show_plots(data):
    fig = plt.figure(figsize=(10, 10))
    for plant in range(len(data)):
        a = fig.add_subplot(len(data), 1, plant + 1)
        a.plot(data[plant])

    plt.show()


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
    list = []

    for col in range(3):
        for row in range(3):
            list.append(image[vert * col: vert * (col + 1),
                        hor * row: hor * (row + 1)])

    return list


def count_green_pixels(img):
    # s_time = time.time()

    hsv_image = rgb2hsv(img)
    saturation = hsv_image[:, :, 1]
    threshold = threshold_otsu(saturation)
    saturation = saturation > threshold
    saturation = median(saturation, disk(2))

    # show_image(saturation)

    # print(str(time.time() - s_time))
    pixels_count = saturation.mean() * saturation.shape[0] * saturation.shape[1] / saturation.max()
    return pixels_count


def count_pixel_square(img):
    one_square = count_green_pixels(img) // 2
    return 1 / one_square


def calculate_squares(desk, storage):
    '''
    Adds calculated squares of plants' leafs from the desk to the storage
    |0|1|2|
    |3| | |
    |4|5|6| i.e. excluding reference square and empty part

    :param desk: image of a desk with plants
    :param storage: array
    :return:
    '''
    parts = split_into_9_parts(desk)
    pixels_count = []
    pixel_square = count_pixel_square(parts[4])

    for n in range(9):
        if (n == 4) or (n == 5):  # skipping reference square and empty part
            continue

        pixels_count.append(count_green_pixels(parts[n]))

    squares = [c * pixel_square for c in pixels_count]

    for part in range(7):
        storage[part].append(squares[part])


images = import_images('6_plant')
images.__next__()  # skip one image (it's blurred)
# for i in range(250):
#     images.__next__()

plants_growth = [[] for i in range(7)]

counter = 25
for desk in images:
    calculate_squares(desk, plants_growth)

    counter -= 1
    if counter < 1:
        break

#     # break  # trying only 1 image


for pl in plants_growth:
    pl = np.array(pl)
    print(pl.mean())

show_plots(plants_growth)

