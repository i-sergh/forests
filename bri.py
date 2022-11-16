import cv2
import numpy as np
# подключение видео
cap = cv2.VideoCapture('forest.mp4')



while True:
    
    # чтение кадра
    tr, frame = cap.read()
    frame = cv2.blur(frame, (40, 40))
    # когда видео закончилось (не удалось считать кадр)
    if not tr:
        # то перезапускаем видео
        cap = cv2.VideoCapture('forest.mp4')
        tr, frame = cap.read()
    # Задаём все холсты для отрисовочки    
    # якость и насыщенность 
    brightness = np.zeros(frame.shape, dtype=np.uint8())
    satur = np.zeros(frame.shape, dtype=np.uint8())
    # якость и насыщенность только точки
    brightness_ = np.zeros(frame.shape, dtype=np.uint8())
    satur_ = np.zeros(frame.shape, dtype=np.uint8())

    # конвентируем в HSV 
    frame_bgr = cv2.cvtColor (frame, cv2.COLOR_BGR2HSV)

    # заполняем соответствующие массивы из основного изо
    brightness[:, :, 0] = frame_bgr[:,:,1]
    brightness[:, :, 1] = frame_bgr[:,:,1]
    brightness[:, :, 2] = frame_bgr[:,:,1]
    satur[:, :, 0] = frame_bgr[:,:,2]
    satur[:, :, 1] = frame_bgr[:,:,2]
    satur[:, :, 2] = frame_bgr[:,:,2]

    # Расставляем точки метки
    # каждая точка расчитывается по среднему значению внутри квадрата 
    # Размер заданного квадрата 50x50
    for i in range(50, frame.shape[0], 50):
        for j in range(50, frame.shape[1], 50):
            # находим среднее значение для яркости и насыщенности по отдельности
            clr = np.mean(brightness[i-50:i, j-50:j, :])
            clr2 = np.mean(satur[i-50, j-50, :])
            # для отображения цветов 
            mark = clr
            mark2 = clr2
            # определяем порог разности между яркостью и контрастностью
            if np.abs(clr -clr2)> 120:
                mark = 255
                mark2 = 255

            # отрисовываем кружочки
            cv2.circle(brightness, (j-25,i-25), 5,
                       (clr,clr,mark), -1)
            cv2.circle(brightness_, (j-25,i-25), 5,
                       (clr,clr,mark), -1)
            
            cv2.circle(satur, (j-25,i-25), 5, 
                       (mark2,clr2,clr2), -1)
            cv2.circle(satur_, (j-25,i-25), 5,
                       (mark2,clr2,clr2), -1)

            if not mark == clr:
                cv2.circle(brightness, (j-25,i-25), 5,
                     (0,255,0), 2)
            if not mark2 == clr2:
                cv2.circle(satur, (j-25,i-25), 5,
                     (0,255,0), 2)
            
    # показываем кадр
    cv2.imshow('original', frame)
    cv2.imshow('br', brightness)
    cv2.imshow('st', satur)
    cv2.imshow('br_', brightness_)
    cv2.imshow('st_', satur_)
    # закрываем видео по нажатию на ESC
    key = cv2.waitKey(1)
    if key == 27:
        break
    if key == 32:
        cv2.waitKey(0)
cv2.destroyAllWindows()
    
