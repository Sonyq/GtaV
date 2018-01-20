#! python3
import numpy as np
#from PIL import ImageGrab
from grabscreen import grab_screen
import cv2
import time

from numpy import ones,vstack
from numpy.linalg import lstsq

from directkeys import PressKey,ReleaseKey, W, A, S, D
from statistics import mean


#def draw_lines(img,lines): #dibujo las lineas en pantalla
#    try: #por si no hay lineas en el array
#        for line in lines:
#            coords = line[0] #el array tiene este formato [[[x1,y1,x2,y2]],[[x1,y1,x2,y2]]]
#            cv2.line(img,(coords[0],coords[1]),(coords[2],coords[3]),[255,255,255],3) #dibujo la linea sup,iniciio,fin,color,ancho
#    except:
#        pass
#

def draw_lanes(img, lines, color=[0, 255, 255], thickness=3):
    # if this fails, go with some default line
    try:

        # finds the maximum y value for a lane marker
        # (since we cannot assume the horizon will always be at the same point.)

        ys = []
        for i in lines:
            for ii in i:
                ys += [ii[1], ii[3]]
        min_y = min(ys)
        max_y = 600
        new_lines = []
        line_dict = {}

        for idx, i in enumerate(lines):
            for xyxy in i:
                # These four lines:
                # modified from http://stackoverflow.com/questions/21565994/method-to-return-the-equation-of-a-straight-line-given-two-points
                # Used to calculate the definition of a line, given two sets of coords.
                x_coords = (xyxy[0], xyxy[2])
                y_coords = (xyxy[1], xyxy[3])
                A = vstack([x_coords, ones(len(x_coords))]).T
                m, b = lstsq(A, y_coords)[0]

                # Calculating our new, and improved, xs
                x1 = (min_y - b) / m
                x2 = (max_y - b) / m

                line_dict[idx] = [m, b, [int(x1), min_y, int(x2), max_y]]
                new_lines.append([int(x1), min_y, int(x2), max_y])

        final_lanes = {}

        for idx in line_dict:
            final_lanes_copy = final_lanes.copy()
            m = line_dict[idx][0]
            b = line_dict[idx][1]
            line = line_dict[idx][2]

            if len(final_lanes) == 0:
                final_lanes[m] = [[m, b, line]]

            else:
                found_copy = False

                for other_ms in final_lanes_copy:

                    if not found_copy:
                        if abs(other_ms * 1.2) > abs(m) > abs(other_ms * 0.8):
                            if abs(final_lanes_copy[other_ms][0][1] * 1.2) > abs(b) > abs(
                                            final_lanes_copy[other_ms][0][1] * 0.8):
                                final_lanes[other_ms].append([m, b, line])
                                found_copy = True
                                break
                        else:
                            final_lanes[m] = [[m, b, line]]

        line_counter = {}

        for lanes in final_lanes:
            line_counter[lanes] = len(final_lanes[lanes])

        top_lanes = sorted(line_counter.items(), key=lambda item: item[1])[::-1][:2]

        lane1_id = top_lanes[0][0]
        lane2_id = top_lanes[1][0]

        def average_lane(lane_data):
            x1s = []
            y1s = []
            x2s = []
            y2s = []
            for data in lane_data:
                x1s.append(data[2][0])
                y1s.append(data[2][1])
                x2s.append(data[2][2])
                y2s.append(data[2][3])
            return int(mean(x1s)), int(mean(y1s)), int(mean(x2s)), int(mean(y2s))

        l1_x1, l1_y1, l1_x2, l1_y2 = average_lane(final_lanes[lane1_id])
        l2_x1, l2_y1, l2_x2, l2_y2 = average_lane(final_lanes[lane2_id])

        return [l1_x1, l1_y1, l1_x2, l1_y2], [l2_x1, l2_y1, l2_x2, l2_y2], lane1_id, lane2_id #devuelvo las dos lineas y sus angulos
    except Exception as e:
        print(str(e))

def roi(img,vertices):      #REGION OF INTEREST *ROI*
    mask = np.zeros_like(img)  #mask es un array igual al array de la imagen pero tod0 negro (lleno de ceros)
    cv2.fillPoly(mask,vertices,255) #sobre el array de ceros pinto un poligono con los puntos de "vertices" y color 255(binario 1111111 blanco)
    masked = cv2.bitwise_and(img,mask) #operacion and (a nivel valores binarios) entre los array de la imagen y la mascara,esto deja negro las partes q estan fuera del poligono
    return masked

def process_img(image):   #funcion que pasa la imagen por un filtro de edges
    original_image = image
    #processed_img = cv2.cvtColor(original_image,cv2.COLOR_BGR2GRAY) #pasa la imagen a gris # Canny ya la pasa a gris esta al dope.
    processed_img = cv2.Canny(original_image,threshold1=200,threshold2=300) #filtro de edges
    processed_img = cv2.GaussianBlur(processed_img, (5, 5), 0) #blureo la imagen para q los pixeles se unan
    ##aplico la region roi
    #vertices = np.array([[10,500],[10,300], [300,200], [500,200], [800,300], [800,500]], np.int32)#vertices del poligono #cambiar esto de lugar re defino al pedo en cada frame
    vertices = np.array([[10, 475], [10, 300], [300, 200], [500, 200], [800, 300], [800, 475]], np.int32)
    processed_img=roi(processed_img,[vertices]) #aplico el roi a la imagen

    ## deteccion de lineas y grafico
    lines = cv2.HoughLinesP(processed_img,1,np.pi/180,180,np.array([]),22,7) #busca las lineas en la imagen, ultimos dos parametros tamanio minimo q tiene q tener una linea
    #y gap maximo entre dos lineas para ser una sola

    m1 = 0
    m2 = 0
    try:
        l1, l2, m1, m2 = draw_lanes(original_image, lines)
        cv2.line(original_image, (l1[0], l1[1]), (l1[2], l1[3]), [0, 255, 0], 30)
        cv2.line(original_image, (l2[0], l2[1]), (l2[2], l2[3]), [0, 255, 0], 30)
    except Exception as e:
        print(str(e))
        pass
    try:
        for coords in lines:
            coords = coords[0]
            try:
                cv2.line(processed_img, (coords[0], coords[1]), (coords[2], coords[3]), [255, 0, 0], 3)
            except Exception as e:
                print(str(e))
    except Exception as e:
        pass

    return processed_img, original_image, m1, m2

def straight():
    PressKey(W)
    ReleaseKey(A)
    ReleaseKey(D)

def left():
    PressKey(A)
    ReleaseKey(W)
    ReleaseKey(D)

def right():
    PressKey(D)
    ReleaseKey(A)
    ReleaseKey(W)

def slow_ya_roll():
    ReleaseKey(W)
    ReleaseKey(A)
    ReleaseKey(D)


for i in list(range(4))[::-1]:
    print(i+1)
    time.sleep(1)

def screen_record():
    last_time = time.time()
    selfdrive = True
    while(True):
        # 800x600 windowed mode for GTA 5, at the top left position of your main screen.
        # 40 px accounts for title bar.
        #printscreen =  np.array(ImageGrab.grab(bbox=(0,40,800,640)))   ##toma la imagen en tal dimencion
        printscreen = grab_screen(region=(0,40,800,640))
        new_screen,original,m1,m2 = process_img(printscreen)
        print('loop took {} seconds'.format(time.time()-last_time))
        lastd_time = time.time()
        #cv2.imshow('window',cv2.cvtColor(printscreen, cv2.COLOR_BGR2RGB))  #convierte el color de la imagen y la muestra en pantalla
        cv2.imshow('window',new_screen)
        cv2.imshow('window2', cv2.cvtColor(original, cv2.COLOR_BGR2RGB))
        if selfdrive:

            if m1 < 0 and m2 < 0:
                right()
            elif m1 > 0 and m2 > 0:
                left()
            else:
                straight()

        if cv2.waitKey(25) & 0xFF == ord('q'):           #teclas para cerrar la pantalla
            cv2.destroyAllWindows()                      #cierrra la screen
            break

screen_record()