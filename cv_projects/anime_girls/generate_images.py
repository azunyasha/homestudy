from PIL import Image
import os
import random

bck_path = "./cv_projects/anime_girls/backgrounds/"
girl_path = "./cv_projects/anime_girls/images/"
output_path = "./cv_projects/anime_girls/output/"

#bck_size = [300,300]
#girl_size = [100,100]

backgrounds = [bck_path + file for file in os.listdir(bck_path)]
girls = [girl_path + file for file in os.listdir(girl_path)]

print(backgrounds[:3])
print(girls[:3])

if not os.path.exists(output_path):
    os.makedirs(output_path)

def make_image(bck_path, girl_path):
    bck_img = Image.open(bck_path)
    girl_img = Image.open(girl_path)
    insert_coord = (
        random.randint(0,bck_img.size[0] - girl_img.size[0]),
        random.randint(0,bck_img.size[1] - girl_img.size[1])
    )
    bck_img.paste(girl_img, insert_coord)
    #print(insert_coord)
    caption_arr = [
        float(insert_coord[0] + girl_img.size[0]/2)/bck_img.size[0],
        float(insert_coord[1] + girl_img.size[1]/2)/bck_img.size[1],
        float(girl_img.size[0]) / bck_img.size[0],
        float(girl_img.size[0]) / bck_img.size[1]
    ]
    caption = f"0 {caption_arr[0]} {caption_arr[1]} {caption_arr[2]} {caption_arr[3]}\n"
    return bck_img, caption

for num, girl_path in enumerate(girls):
    try:
        bck_path = random.choice(backgrounds)
        out_img, caption = make_image(bck_path,girl_path)
        out_img.save(output_path + str(num) + ".jpg")
        with open(output_path + str(num) + ".txt", 'w') as output_file:
            output_file.write(caption)
            output_file.close()
    except Exception as e:
        print(num, girl_path)
        print(e)
