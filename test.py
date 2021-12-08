import cv2, dlib
import numpy as np
import tensorflow as tf
from imutils import face_utils
# from keras.models import load_model
import time
import speaker
import switchControl as switch

IMG_SIZE = (34, 26)
model_path = 'models/2018_12_17_22_58_35.h5'


def crop_eye(gray, eye_points):
    x1, y1 = np.amin(eye_points, axis=0)
    x2, y2 = np.amax(eye_points, axis=0)
    cx, cy = (x1 + x2) / 2, (y1 + y2) / 2

    w = (x2 - x1) * 1.2
    h = w * IMG_SIZE[1] / IMG_SIZE[0]

    margin_x, margin_y = w / 2, h / 2

    min_x, min_y = int(cx - margin_x), int(cy - margin_y)
    max_x, max_y = int(cx + margin_x), int(cy + margin_y)

    eye_rect = np.rint([min_x, min_y, max_x, max_y]).astype(np.int)

    eye_img = gray[eye_rect[1]:eye_rect[3], eye_rect[0]:eye_rect[2]]

    return eye_img, eye_rect


# main
def modelRun(set_value):
    # ------------------- load model -------------------#
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

    model = tf.keras.models.load_model(model_path)

    # ------------------- setting variables -------------------#
    isClosed = False
    sleep_start_time = time.time()
    sleep_end_time = time.time()
    face_start_time = 0
    face_end_time = 0
    closeTime = 0
    faceTime = 0
    countsleep = 0
    validface = False

    # ------------------- run model -------------------#
    cap = cv2.VideoCapture(0)

    while cap.isOpened():
        # ------------------- read -------------------#
        ret, img_ori = cap.read()

        if not ret:
            break

        img_ori = cv2.resize(img_ori, dsize=(0, 0), fx=0.5, fy=0.5)

        img = img_ori.copy()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = detector(gray)

        if len(faces) == 0:
            face_end_time = time.time()
            faceTime = face_end_time - face_start_time
            if validface and faceTime > 10:  # 얼굴이 있다가 없어지면 잔다고 판별
                switch.switchControl(set_value)  # 예약된 값으로 멀티탭 제어하기
                print("잔다고 인식!")
                # ------------------- reset variables -------------------#
                isClosed = False
                sleep_start_time = time.time()
                sleep_end_time = time.time()
                face_start_time = 0
                face_end_time = 0
                closeTime = 0
                faceTime = 0
                countsleep = 0
                validface = False

        else:  # 얼굴 감지
            face_start_time = time.time()
            validface = True

            face = faces[0]
            # ------------------- detected face -------------------#
            shapes = predictor(gray, face)
            shapes = face_utils.shape_to_np(shapes)

            eye_img_l, eye_rect_l = crop_eye(gray, eye_points=shapes[36:42])
            eye_img_r, eye_rect_r = crop_eye(gray, eye_points=shapes[42:48])

            try:
                eye_img_l = cv2.resize(eye_img_l, dsize=IMG_SIZE)
                eye_img_r = cv2.resize(eye_img_r, dsize=IMG_SIZE)
                eye_img_r = cv2.flip(eye_img_r, flipCode=1)

                eye_input_l = eye_img_l.copy().reshape((1, IMG_SIZE[1], IMG_SIZE[0], 1)).astype(np.float32) / 255.
                eye_input_r = eye_img_r.copy().reshape((1, IMG_SIZE[1], IMG_SIZE[0], 1)).astype(np.float32) / 255.

                # ------------------- model predict -------------------#
                pred_l = model.predict(eye_input_l)
                pred_r = model.predict(eye_input_r)

                # visualize
                state_l = 'O %.1f' if pred_l > 0.1 else '- %.1f'
                state_r = 'O %.1f' if pred_r > 0.1 else '- %.1f'

                state_l = state_l % pred_l
                state_r = state_r % pred_r

                # print("state_l: ", state_l)
                # print("state_r: ", state_r)

                cv2.rectangle(img, pt1=tuple(eye_rect_l[0:2]), pt2=tuple(eye_rect_l[2:4]), color=(255, 0, 0),
                              thickness=1)
                cv2.rectangle(img, pt1=tuple(eye_rect_r[0:2]), pt2=tuple(eye_rect_r[2:4]), color=(0, 255, 0),
                              thickness=1)

                cv2.putText(img, state_l, tuple(eye_rect_l[0:2]), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 1)
                cv2.putText(img, state_r, tuple(eye_rect_r[0:2]), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 1)

                # ------------------- detect closed eyes -------------------#
                if (state_l[0] == '-') and (state_r[0] == '-'):  # 눈을 감음
                    print("close eye")
                    if not isClosed:  # 이전에 눈을 감고 있지 않았다면
                        isClosed = True
                        sleep_start_time = time.time()  # start
                    else:  # 이전에 눈을 감고 있었다면
                        sleep_end_time = time.time()
                    closeTime = sleep_end_time - sleep_start_time

                    if (closeTime > 3.0) and (closeTime < 10.0) and (countsleep < 2):
                        countsleep = countsleep + 1
                        speaker.ringAlarm()
                        isClosed = False

                elif (state_l[0] == 'O') and (state_r[0] == 'O'):  # 눈을 뜸
                    isClosed = False
                    closeTime = 0

                # print("closeTime: ", closeTime)
                # print("countsleep: ", countsleep)

                if (closeTime > 10.0):  # 잠
                    switch.switchControl(set_value)  # 예약된 값으로 멀티탭 제어하기
                    print("잔다고 인식!")

            except cv2.error as e:
                print("fail detecting eyes!")
                pass

        # cv2.imshow('result', img)

        if cv2.waitKey(1) == ord('q'):
            break
