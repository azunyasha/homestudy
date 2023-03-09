from PIL import Image, ImageFilter, ImageDraw
import os
import random

bck_path = "./cv_projects/anime_girls/backgrounds/"
girl_path = "./cv_projects/anime_girls/images/"
output_path = "./cv_projects/anime_girls/output/"

paths = [
    "./cv_projects/anime_girls/output/test",
    "./cv_projects/anime_girls/output/test/images",
    "./cv_projects/anime_girls/output/test/labels",
    "./cv_projects/anime_girls/output/train",
    "./cv_projects/anime_girls/output/train/images",
    "./cv_projects/anime_girls/output/train/labels",
    "./cv_projects/anime_girls/output/valid",
    "./cv_projects/anime_girls/output/valid/images",
    "./cv_projects/anime_girls/output/valid/labels"
]
#bck_size = [300,300]
#girl_size = [100,100]

backgrounds = [bck_path + file for file in os.listdir(bck_path)]
girls = [girl_path + file for file in os.listdir(girl_path)]

print(backgrounds[:3])
print(girls[:3])

for path in paths:
    if not os.path.exists(path):
        os.makedirs(path)
if not os.path.exists(output_path):
    os.makedirs(output_path)

def make_image(bck_path, girl_path):
    bck_img = Image.open(bck_path)
    girl_img = Image.open(girl_path)
    mask_img = Image.new("L", girl_img.size, 0)
    draw = ImageDraw.Draw(mask_img)
    new_size = random.randint(20,250)

    draw.ellipse((10, 10, 90, 90), fill=255)
    mask_img = mask_img.filter(ImageFilter.GaussianBlur(7))
    girl_img = girl_img.resize((new_size,new_size))
    mask_img = mask_img.resize((new_size,new_size))


    insert_coord = (
        random.randint(0,bck_img.size[0] - girl_img.size[0]),
        random.randint(0,bck_img.size[1] - girl_img.size[1])
    )
    bck_img.paste(girl_img, insert_coord, mask_img)
    #print(insert_coord)
    caption_arr = [
        float(insert_coord[0] + girl_img.size[0]/2)/bck_img.size[0],
        float(insert_coord[1] + girl_img.size[1]/2)/bck_img.size[1],
        float(girl_img.size[0]) / bck_img.size[0] / 1.4,
        float(girl_img.size[0]) / bck_img.size[1] / 1.4
    ]
    caption = f"0 {caption_arr[0]} {caption_arr[1]} {caption_arr[2]} {caption_arr[3]}\n"
    return bck_img, caption
test_num = 0.1
train_num = 0.9
valid_num = 1
for i in range(5):
    for num, girl_path in enumerate(girls):
        if num < test_num * len(girls):
            output_path_full = output_path + "test/"
        elif num < train_num * len(girls):
            output_path_full = output_path + "train/"
        else:
            output_path_full = output_path + "valid/"
        try:
            bck_path = random.choice(backgrounds)
            out_img, caption = make_image(bck_path,girl_path)
            out_img.save(output_path_full + "images/" + str(num*(i+1)) + ".jpg")
            with open(output_path_full + "labels/" + str(num*(i+1)) + ".txt", 'w') as output_file:
                output_file.write(caption)
                output_file.close()
        except Exception as e:
            print(num*(i+1), girl_path)
            print(e)
