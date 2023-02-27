from PIL import Image
import os

prj_path = "./cv_projects/anime_girls/images/"



for file_name in os.listdir(prj_path):
  try:
      img = Image.open(prj_path + file_name)
      img = img.resize((100, 100))
      img.save(prj_path + file_name)
  except Exception as e:
      print(f'failed: {file_name}')
      print(e)
