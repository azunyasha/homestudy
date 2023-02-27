import urllib.request
import os

project_path = "./cv_projects/anime_girls/"
with open(project_path + "href_list.txt", "r") as file:
    href_list = file.read().split()
    file.close()
stop_list = [
    "https://i.pinimg.com/70x",
    "https://i.pinimg.com/30x30_RS",
    "https://i.pinimg.com/75x"
]
href_list_output = []
for num, href in enumerate(href_list):
    if not any([stop_word in href for stop_word in stop_list]):
        href_list_output += [href]

print(f'len: {len(href_list_output)}')
print(href_list_output[:3])
output_path = project_path + "images/"
if not os.path.exists(output_path):
    os.makedirs(output_path)

for num, href in enumerate(href_list_output[:5]):
    filename = output_path + str(num) + ".jpg"
    urllib.request.urlretrieve(href, filename)
print("success")
