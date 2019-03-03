import matplotlib.pyplot as plt

from skimage import data
from skimage.color import rgb2gray
from skimage.filters import try_all_threshold


def show_all_thresholds(img):
    ''' Tests several thresholds to an image and shows plots '''
    # img = data.page()
    # img = rgb2gray(img)
    # print(img.shape)

    fig, ax = try_all_threshold(img, figsize=(10, 8), verbose=False)
    plt.show()

