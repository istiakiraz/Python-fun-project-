import cv2
import mediapipe as mp
import pyautogui
import time

cap = cv2.VideoCapture(0)
hand_detector = mp.solutions.hands.Hands()
drawing_utils = mp.solutions.drawing_utils
screen_width, screen_height = pyautogui.size()
index_y = 0

last_click_time = 0
click_count = 0


def detect_double_tap(current_time):
    global last_click_time, click_count
    if current_time - last_click_time < 0.3:
        click_count += 1
        if click_count == 2:
            pyautogui.doubleClick()
            click_count = 0
    else:
        click_count = 1
    last_click_time = current_time


while True:
    _, frame = cap.read()
    frame_height, frame_width, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = hand_detector.process(rgb_frame)
    hands = output.multi_hand_landmarks

    if hands:
        for hand in hands:
            drawing_utils.draw_landmarks(frame, hand)
            landmarks = hand.landmark
            index_x = index_y = thumb_x = thumb_y = None
            for id, landmark in enumerate(landmarks):
                x = int(landmark.x * frame_width)
                y = int(landmark.y * frame_height)

                if id == 8:
                    cv2.circle(img=frame, center=(x, y), radius=10, color=(0, 255, 255))
                    index_x = screen_width / frame_width * x
                    index_y = screen_height / frame_height * y

                if id == 4:
                    cv2.circle(img=frame, center=(x, y), radius=10, color=(0, 255, 255))
                    thumb_x = screen_width / frame_width * x
                    thumb_y = screen_height / frame_height * y

            if index_x is not None and thumb_x is not None:
                distance = abs(index_y - thumb_y)
                print('Distance:', distance)

                if distance < 20:
                    detect_double_tap(time.time())
                elif distance < 100:
                    pyautogui.moveTo(index_x, index_y)

    cv2.imshow('Virtual Mouse', frame)
    cv2.waitKey(1)
