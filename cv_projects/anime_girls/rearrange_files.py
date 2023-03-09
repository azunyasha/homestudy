import os
from os import walk

prj_path = "./cv_projects/anime_girls/output"

os.chdir(prj_path)

os.mkdir("./yolov5")
os.mkdir("./yolov5/datasets")
os.mkdir("./yolov5/datasets/test")
os.mkdir("./yolov5/datasets/train")
os.mkdir("./yolov5/datasets/valid")
os.mkdir("./yolov5/datasets/test/images")
os.mkdir("./yolov5/datasets/test/labels")
os.mkdir("./yolov5/datasets/train/images")
os.mkdir("./yolov5/datasets/train/labels")
os.mkdir("./yolov5/datasets/valid/images")
os.mkdir("./yolov5/datasets/valid/labels")

#filenames = next(walk(prj_path), (None, None, []))[2]  # [] if no file
#images = []
#for name in filenames:
#  images += [np.array(Image.open(path+"/"+name))]

import shutil


files = []
images = []



for dirname, _, filenames in os.walk('./'):
    for filename in filenames:
        print(filename)
        if filename[-3:] == 'jpg':

            #files += [os.path.join(dirname, filename)[:-5]]
            files += [filename[:-4]]
            #images += [np.array(Image.open(os.path.join(dirname, filename)))]
            dir_name = dirname
print(files)

for i,file in enumerate(files):
    if i % 100 == 0:
        print(i)

    if i<len(files)*0.1:
        shutil.copyfile(dir_name+"/"+file+".jpg", "./yolov5/datasets/test/images/"+file+".jpg")
        shutil.copyfile(dir_name+"/"+file+".txt", "./yolov5/datasets/test/labels/"+file+".txt")
    elif i<len(files)*0.8:
        shutil.copyfile(dir_name+"/"+file+".jpg", "./yolov5/datasets/train/images/"+file+".jpg")
        shutil.copyfile(dir_name+"/"+file+".txt", "./yolov5/datasets/train/labels/"+file+".txt")
    else:
        shutil.copyfile(dir_name+"/"+file+".jpg", "./yolov5/datasets/valid/images/"+file+".jpg")
        shutil.copyfile(dir_name+"/"+file+".txt", "./yolov5/datasets/valid/labels/"+file+".txt")
