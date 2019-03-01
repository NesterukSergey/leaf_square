'''
This script makes a folder with photos of the selected plant.

Searches in subdirectories of all_photos directory. Copies photos of a plant
at the selected position {1...6}

In presented dataset it means selecting photos of plants
that are fed with the same nutrient solution
'''

import os
import shutil
from shutil import copyfile


def copy_selected_plant(source_folder, plant_number=6):
    init_folder = os.getcwd()
    # print(init_folder)

    if not os.path.exists(source_folder):
        print('No source file fount')
        return

    new_folder = str(plant_number) + "_plant"
    if os.path.exists(new_folder):
        shutil.rmtree(new_folder)

        ## if you do not want to remove existing files
        # print('Destination folder already exists')
        # return

    os.mkdir(new_folder)

    os.chdir(source_folder)

    for folder in os.listdir(os.getcwd()):
        # setting destination photos' name to the source folders' name
        # excluding prefix
        photo_name = folder[9:] + '.jpg'
        selected_photo_path = os.path.join(folder, 'photo' + str(plant_number) + 's.jpg')

        if not os.path.exists(selected_photo_path):
            print('No ' + selected_photo_path + ' file found')
            continue
        copyfile(selected_photo_path, os.path.join(init_folder, new_folder, photo_name))

    os.chdir(init_folder)


copy_selected_plant('all_photos', 6)
