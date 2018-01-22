import numpy as np
import os
#import pandas as pd
#from collections import Counter

w = [1,0,0,0,0,0,0,0,0]
s = [0,1,0,0,0,0,0,0,0]
a = [0,0,1,0,0,0,0,0,0]
d = [0,0,0,1,0,0,0,0,0]
wa = [0,0,0,0,1,0,0,0,0]
wd = [0,0,0,0,0,1,0,0,0]
sa = [0,0,0,0,0,0,1,0,0]
sd = [0,0,0,0,0,0,0,1,0]
nk = [0,0,0,0,0,0,0,0,1]

dirs = os.listdir("./datasets")

lefts = []
rights = []
forwards = []
rare = []
total_samples = 0
i=0
balanced_data = []
for dir_dataset in dirs:
    i+=1
    print("processing dataset {} of {}".format(i,len(dirs)))
    train_data = np.load("datasets/{}".format(dir_dataset))
    np.random.shuffle(train_data)
    total_samples += len(train_data)

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

balanced_data += forwards
balanced_data += lefts
balanced_data += rights
balanced_data += rare

np.random.shuffle(balanced_data)
print("total samples: "+str(total_samples))
print("balanced data: "+str(len(balanced_data)))
print("please wait saving data...")
np.save('balanced_data.npy',balanced_data)
print("done!(but wait until the f**king process ends)")

