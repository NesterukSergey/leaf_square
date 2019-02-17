import time
import os
from skimage import io
from LeafRGB import LeafRGB

import collections
c = collections.Counter()


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

s_time = time.time()

for img in images:
    l = LeafRGB(img)
    l.show_all()

    break  # trying only 1 image

# print(str(time.time() - s_time) + " for 4 images")
print(str(time.time() - s_time))
