import time
import os
from skimage import io
from LeafRGB import LeafRGB
from LeafHSV import LeafHSV


def import_images():
    '''
    Imports images from "/testDataset/"

    Returns:
    img_list (list of numpy.ndarrays): the list of images
    '''
    img_list = []

    # Hardcoded filenames
    filenames_list = ['photo1s.jpg', 'photo2s.jpg', 'photo3s.jpg', 'photo4s.jpg']
    for filename in filenames_list:
        file = os.path.join('testDataset', filename)
        img_list.append(io.imread(file))

    return img_list


images = import_images()



for img in images:
    s_time = time.time()

    rgb = LeafRGB(img)
    # rgb.show_all()
    # print(rgb.green_square)
    print(str(time.time() - s_time))
    s_time = time.time()

    hsv = LeafHSV(img)
    # hsv.show_all()
    # print(hsv.green_square)

    print(str(time.time() - s_time))

    # break  # trying only 1 image


