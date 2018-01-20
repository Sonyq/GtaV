# train_model.py

import numpy as np
from alexnet import alexnet
#import cv2
WIDTH = 160
HEIGHT = 120
LR = 1e-3
EPOCHS = 10
MODEL_NAME = 'pygta5-bike-{}-{}-{}-epochs-7K-data.model'.format(LR, 'alexnetv2',EPOCHS)

model = alexnet(HEIGHT,WIDTH, LR)


train_data = np.load('balanced_data1.npy')

train = train_data[:-500] #datos q voy a usar para entrenar
test = train_data[-500:] #uso los ultimos 500 datos para testear el entrenamiento de la ia

X = np.array([i[0] for i in train]).reshape(-1,HEIGHT,WIDTH,1) #el ancho y alto estaban al reves
#cv2.imwrite('testt.png',X[1]) #solo para chequear q las imagenes esten bien
Y = [i[1] for i in train]

test_x = np.array([i[0] for i in test]).reshape(-1,HEIGHT,WIDTH,1)
test_y = [i[1] for i in test]

model.fit({'input': X}, {'targets': Y}, n_epoch=EPOCHS, validation_set=({'input': test_x}, {'targets': test_y}),
    snapshot_step=500, show_metric=True, run_id=MODEL_NAME)

model.save(MODEL_NAME)



# tensorboard --logdir=foo:C:\directiorio\de la\carpeta\del proyecto\log


#python C:\Users\Sony-q\Anaconda3\Lib\site-packages\tensorboard\main.py --logdir=foo:C:\directiorio\de la\carpeta\del proyecto\log #usa este comando desde consola para ver la tensorboard