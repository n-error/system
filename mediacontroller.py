import cv2
import mediapipe as mp
import pyautogui
import time

class HandGestureController:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.drawing = mp.solutions.drawing_utils
        self.hands = mp.solutions.hands
        self.hand_obj = self.hands.Hands(max_num_hands=1)
        self.start_init = False
        self.prev = -1

    def count_fingers(self, lst):
        cnt = 0
        thresh = (lst.landmark[0].y * 100 - lst.landmark[9].y * 100) / 2

        if (lst.landmark[5].y * 100 - lst.landmark[8].y * 100) > thresh:
            cnt += 1

        if (lst.landmark[9].y * 100 - lst.landmark[12].y * 100) > thresh:
            cnt += 1

        if (lst.landmark[13].y * 100 - lst.landmark[16].y * 100) > thresh:
            cnt += 1

        if (lst.landmark[17].y * 100 - lst.landmark[20].y * 100) > thresh:
            cnt += 1

        if (lst.landmark[5].x * 100 - lst.landmark[4].x * 100) > 6:
            cnt += 1

        return cnt

    def handle_gesture(self, finger_count):
        # Add your gesture handling logic here
        if finger_count == 1:
            pyautogui.press("right")
        elif finger_count == 2:
            pyautogui.press("left")
        elif finger_count == 3:
            pyautogui.press("up")
        elif finger_count == 4:
            pyautogui.press("down")
        elif finger_count == 5:
            pyautogui.press("space")

    def process_gestures(self):
        while True:
            end_time = time.time()
            _, frm = self.cap.read()
            frm = cv2.flip(frm, 1)

            res = self.hand_obj.process(cv2.cvtColor(frm, cv2.COLOR_BGR2RGB))

            if res.multi_hand_landmarks:
                hand_key_points = res.multi_hand_landmarks[0]
                cnt = self.count_fingers(hand_key_points)

                if not (self.prev == cnt):
                    if not (self.start_init):
                        start_time = time.time()
                        self.start_init = True

                    elif (end_time - start_time) > 0.2:
                        self.handle_gesture(cnt)
                        self.prev = cnt
                        self.start_init = False

                self.drawing.draw_landmarks(frm, hand_key_points, self.hands.HAND_CONNECTIONS)

            cv2.imshow("window", frm)

            if cv2.waitKey(1) == 27:
                cv2.destroyAllWindows()
                self.cap.release()
                break

if __name__ == "__main__":
    hand_gesture_controller = HandGestureController()
    hand_gesture_controller.process_gestures()