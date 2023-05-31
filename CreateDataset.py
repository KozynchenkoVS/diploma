# Библиотеки
import Augmentor
import os
from PIL import Image
import shutil
import splitfolders
#Функция аугментации изображений в папке
def augment_images(folder, num):
    for animal in folder:
        print("Augmenting ", animal)
        augmentator = Augmentor.Pipeline(animal)
        augmentator.rotate(0.4, max_left_rotation=5, max_right_rotation=5)
        p_flip = 0.65
        augmentator.flip_left_right(probability=p_flip)
        p_skew = 0.55
        augmentator.skew_left_right(probability=p_skew, magnitude=0.1)
        p_zoom = 0.65
        augmentator.zoom(probability=p_zoom, min_factor=1.1, max_factor=1.1)
        p_erase = 0.65
        augmentator.random_erasing(probability=p_erase,rectangle_area=0.2)
        p_bright = 0.60
        augmentator.random_brightness(probability=p_bright, min_factor=1.15, max_factor=1.2)
        p_contrast = 0.55
        augmentator.random_contrast(probability=p_contrast, min_factor=1.1, max_factor=1.25)
        augmentator.sample(num)
def extract_augment_output(folders):
    for folder in folders:
        images = [file for file in os.listdir(folder+"output")]
        for image in images:
            shutil.move(folder+"output/"+image, folder)
def extract_not_augmented(folders):
    not_augmented = []
    for folder in folders:
        if os.path.exists(folder + "output"):
            if len(os.listdir(folder + "output")) < 50:
                # shutil.rmtree(folder + "output")
                not_augmented.append(folder)
            else: continue
        else: not_augmented.append(folder)
    return not_augmented
splitfolders.ratio("newTrainModel", output="newTrainModelSplit", seed=42, ratio=(.7, .15, .15))
path = "newTrainModelSplit/train"
birds = os.listdir(path)
animals = [path + "/" + folder + "/" for folder in birds]
# print(birds)
augment_images(animals, 100)
extract_augment_output(animals)