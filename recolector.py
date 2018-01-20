#! python3
import numpy as np
from grabscreen import grab_screen
import cv2
import time

from getkeys import key_check
import os

w = [1,0,0,0,0,0,0,0,0]
s = [0,1,0,0,0,0,0,0,0]
a = [0,0,1,0,0,0,0,0,0]
d = [0,0,0,1,0,0,0,0,0]
wa = [0,0,0,0,1,0,0,0,0]
wd = [0,0,0,0,0,1,0,0,0]
sa = [0,0,0,0,0,0,1,0,0]
sd = [0,0,0,0,0,0,0,1,0]
nk = [0,0,0,0,0,0,0,0,1]

def keys_to_output(keys):
    '''
    Convert keys to a ...multi-hot... array
     0  1  2  3  4   5   6   7    8
    [W, S, A, D, WA, WD, SA, SD, NOKEY] boolean values.
    '''

    if 'W' in keys and 'A' in keys:
        output = wa
    elif 'W' in keys and 'D' in keys:
        output = wd
    elif 'W' in keys:
        output = w
    elif 'S' in keys:
        output = s
    elif 'A' in keys:
        output = a
    elif 'D' in keys:
        output = d
    else:
        output = nk
    return output

file_name = "training_data.npy"
if os.path.isfile(file_name):
    print("el archivo existe")
    training_data = list(np.load(file_name))
else:
    print("el archivo no existe, lo creo")
    training_data = []

def screen_record():
    for i in list(range(4))[::-1]:
        print(i + 1)
        time.sleep(1)

    last_time = time.time()
    paused = False
    while(True):
        if not paused:
            screen = grab_screen(region=(0,40,800,600))
            screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
            screen = cv2.resize(screen, (160, 120))
            #print('loop took {} seconds'.format(time.time()-last_time))
            #last_time = time.time()
            keys = key_check()
            output = keys_to_output(keys)
            training_data.append([screen,output])

            if len(training_data) % 600 == 0:
                print(len(training_data))
                np.save(file_name,training_data)

        keys = key_check()
        if 'T' in keys:
            if paused:
                paused = False
                print("despausado")
                time.sleep(1)
            else:
                print("pausado")
                paused = True
                time.sleep(1)

screen_record()