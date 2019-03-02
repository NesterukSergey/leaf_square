import time
import os
from skimage import io
import matplotlib.pyplot as plt

from LeafRGB import LeafRGB
from LeafHSV import LeafHSV
from thresholding import show_all_thresholds


def import_test_images():
    '''
    Imports images from "/testDataset/"

    Returns:
    img_list (list of numpy.ndarrays): the list of images
    '''
    img_list = []

    # Hardcoded test filenames
    filenames_list = ['photo6s.jpg', 'photo1s.jpg', 'photo2s.jpg', 'photo3s.jpg', 'photo4s.jpg']

    for filename in filenames_list:
        file = os.path.join('testDataset', filename)
        img_list.append(io.imread(file))

    return img_list


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


# images = import_test_images()
images = import_images('6_plant')
for img in images:
    parts = split_into_9_parts(img)
    show_image(parts[2])
    break # trying only 1 image

# for img in images:
#     # # testing RGB segmentation
#     # s_time = time.time()
#     # rgb = LeafRGB(img)
#     # rgb.show_all()
#     # print(rgb.green_square)
#     # print(str(time.time() - s_time))
#
#     # # testing HSV segmentation
#     # s_time = time.time()
#     # hsv = LeafHSV(img)
#     # hsv.show_all()
#     # print(hsv.green_square)
#     # print(str(time.time() - s_time))
#
#     show_all_thresholds(img)
#
#     break  # trying only 1 image
