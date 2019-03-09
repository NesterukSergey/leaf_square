import time
import os
from skimage import io
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pandas.plotting import lag_plot
from pandas.plotting import autocorrelation_plot
from pandas import DataFrame
from pandas import concat
from pandas import Series
from statsmodels.graphics.tsaplots import plot_acf
from sklearn.metrics import mean_squared_error
from skimage.filters import threshold_otsu
from skimage.color import rgb2hsv
from skimage.morphology import disk
from skimage.filters.rank import median
import cv2
from statsmodels.tsa.ar_model import AR
from sklearn.metrics import mean_squared_error

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
# copy_selected_plant_photos.copy_selected_plant('all_photos', 6)


# Importing images from dataset
# images = import_images('6_plant')


# Calculating areas of plants on the desk
# count_area.calculate_squares(images)


# Calculating areas of one selected plant on the desk
# count_area.calculate_single_plant(images, 2)


# Getting raw array with areas of one selected plant
# areas = count_area.read_areas_from_file(3, type='array')
# show_plots([areas])


# # Getting Pandas.Series with areas of one selected plant
# areas = count_area.read_areas_from_file(2)
# lag_plot(areas)
# plt.show()


series = Series.from_csv('2_plant_areas.csv', header=0)

# prediction.show_autocorrelation(series)

# prediction.show_baseline(series)




# split dataset
X = series.values
train, test = X[1:len(X)-30], X[len(X)-30:len(X)-20]
# train autoregression
model = AR(train)
model_fit = model.fit()
print('Lag: %s' % model_fit.k_ar)
print('Coefficients: %s' % model_fit.params)
# make predictions
predictions = model_fit.predict(start=len(train), end=len(train)+len(test)-1, dynamic=False)
for i in range(len(predictions)):
    print('predicted=%f, expected=%f' % (predictions[i], test[i]))
error = mean_squared_error(test, predictions)
print('Test MSE: %.3f' % error)
# plot results
plt.plot(test)
plt.plot(predictions, color='red')
plt.show()

