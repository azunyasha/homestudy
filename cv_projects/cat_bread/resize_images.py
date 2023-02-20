from PIL import Image
import os

prj_path = './cv_projects/cat_bread/'
classes = next(os.walk(prj_path))[1]

print(classes)
for class_name in classes:
  path = prj_path + "/" + class_name + "/"
  print(class_name + ":")
  for file_name in os.listdir(path):
      try:
          img = Image.open(path + file_name)
          img = img.resize((100, 100))
          img.save(path + file_name)
          print(f'saved: {class_name}/{file_name}')
      except Exception as e:
          print(f'failed: {class_name}/{file_name}')
          print(e)
