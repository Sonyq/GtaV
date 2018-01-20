import cv2
import numpy as np

train_data = np.load("balanced_data1.npy")

for data in train_data:
    img = data[0]
    choice = data[1]
    print(img.shape)
    cv2.imshow("test",img)
    print(choice)
    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break