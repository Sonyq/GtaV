import numpy as np
import pandas as pd
from collections import Counter
#from random import shuffle
import cv2

w = [1,0,0,0,0,0,0,0,0]
s = [0,1,0,0,0,0,0,0,0]
a = [0,0,1,0,0,0,0,0,0]
d = [0,0,0,1,0,0,0,0,0]
wa = [0,0,0,0,1,0,0,0,0]
wd = [0,0,0,0,0,1,0,0,0]
sa = [0,0,0,0,0,0,1,0,0]
sd = [0,0,0,0,0,0,0,1,0]
nk = [0,0,0,0,0,0,0,0,1]

train_data_m = np.load("training_data_m.npy")
train_data_l = np.load("training_data_l.npy")
tData = [train_data_m,train_data_l]
print(len(train_data_m)+len(train_data_l))
#for train_data in tData:
#    df = pd.DataFrame(train_data)
#    print(df.head())
#    print(Counter(df[1].apply(str)))

lefts = []
rights = []
forwards = []
rare = []

for train_data in tData:
    np.random.shuffle(train_data)

    for data in train_data:
        img = data[0]
        choice = data[1]

        if choice == a or choice == wa:
            lefts.append([img,choice])
        elif choice == w:
            forwards.append([img,choice])
        elif choice == d or choice == wd:
            rights.append([img,choice])
        elif choice == s or choice == nk:
            rare.append([img,choice])
        else:
            print("ninguna accion")

forwards = forwards[:len(lefts)][:len(rights)]
lefts = lefts[:len(forwards)]
rights = rights[:len(forwards)]

balanced_data = forwards + lefts + rights + rare
np.random.shuffle(balanced_data)
print(len(balanced_data))

np.save('balanced_data1.npy',balanced_data)

