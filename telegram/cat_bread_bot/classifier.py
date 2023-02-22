import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

import numpy as np

from PIL import Image

import time
import os


class Net(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(3, 6, 5)
        self.pool = nn.MaxPool2d(2, 2)
        self.conv2 = nn.Conv2d(6, 16, 5)
        self.fc1 = nn.Linear(7744  , 120)
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, 2)

    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = torch.flatten(x, 1) # flatten all dimensions except batch
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x


net = Net()
net.load_state_dict(torch.load("cat_bread.pth"))
criterion = nn.CrossEntropyLoss()
optimizer = optim.SGD(net.parameters(), lr=0.001, momentum=0.9)

input_dir = "./input/"
output_dir = "./output/"
if not os.path.isdir(input_dir):
    os.makedirs(input_dir)
if not os.path.isdir(output_dir):
    os.makedirs(output_dir)

def predict(image):
    input_arr = img_2_array(image)
    input_tensor = torch.FloatTensor(input_arr)
    outputs = net(input_tensor)
    _, predicted = torch.max(outputs, 1)
    classes = ['Эта Хлеп, еш', 'Эта кот, нееш']
    return classes[int(predicted[0])]

def img_2_array(img):
  img_array = [img].copy()
  for num, img in enumerate([img]):
    img_array[num]  = np.array(img.resize((100, 100)))
    img_array[num] = img_array[num] / 255.0 - 0.5
  img_array = np.array(img_array)
  img_array = np.transpose(img_array, (0,3,1,2))
  return img_array


def scheduler():
    file_name_list = os.listdir(input_dir)
    for file_name in file_name_list:
        try:
            img = Image.open(input_dir+file_name)
            img_class = predict(img)
            img.close()
            output_name = output_dir + os.path.splitext(file_name)[0] + ".txt"
            with open(output_name, "w") as text_file:
                text_file.write(img_class)
                text_file.close()

        except Exception as e:
            print(e)
        os.remove(input_dir+file_name)


while True:
    scheduler()
