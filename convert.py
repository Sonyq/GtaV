
import os
import numpy as np
from cv2 import imwrite

def opcion(arr):

    if arr == [1,0,0,0,0,0,0,0,0]:
        return 0
    elif arr == [0,1,0,0,0,0,0,0,0]:
        return 1
    elif arr == [0,0,1,0,0,0,0,0,0]:
        return 2
    elif arr == [0,0,0,1,0,0,0,0,0]:
        return 3
    elif arr == [0,0,0,0,1,0,0,0,0]:
        return 4
    elif arr == [0,0,0,0,0,1,0,0,0]:
        return 5
    elif arr == [0,0,0,0,0,0,1,0,0]:
        return 6
    elif arr == [0,0,0,0,0,0,0,1,0]:
        return 7
    elif arr == [0,0,0,0,0,0,0,0,1]:
        return 8

dirs = os.listdir("./balanced data")
base_file_name = "balanced data/{}"
train_data = []

#new_path = 'train.txt'
new_path = 'val.txt'
file = open(new_path,'w')
#img_dir = "./images/image{}.png"
img_dir = "./valimg/image{}.png"


for dir_bd in dirs:
    # train_data = np.load('balanced_data.npy')
    data = list(np.load(base_file_name.format(dir_bd)))
    train_data += data

for nro,data in enumerate(train_data[85000:]):
    img = data[0]
    choice = data[1]
    imwrite(img_dir.format(nro),img)
    line = "{} {}\n".format(img_dir.format(nro),opcion(choice))
    file.write(line)

file.close()

