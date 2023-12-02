import cv2
import mediapipe as mp
import microcontroller as mic

class CarController:
    def __init__(self):
        self.mp_draw = mp.solutions.drawing_utils
        self.mp_hand = mp.solutions.hands
        self.tip_ids = [4, 8, 12, 16, 20]
        self.hands = self.mp_hand.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)
        self.cap = cv2.VideoCapture(0)  # Default to webcam

    def hand_gesture_control(self):
        while True:
            ret, img = self.cap.read()
            results = self.hands.process(img)

            if results.multi_hand_landmarks:
                lm_list = []
                for hand_landmark in results.multi_hand_landmarks:
                    my_hands = results.multi_hand_landmarks[0]
                    for id, lm in enumerate(my_hands.landmark):
                        h, w, c = img.shape
                        cx, cy = int(lm.x * w), int(lm.y * h)
                        lm_list.append([id, cx, cy])
                    self.mp_draw.draw_landmarks(img, hand_landmark, self.mp_hand.HAND_CONNECTIONS)

                fingers = []
                if lm_list:
                    if lm_list[self.tip_ids[0]][1] > lm_list[self.tip_ids[0] - 1][1]:
                        fingers.append(1)
                    else:
                        fingers.append(0)
                    for id in range(1, 5):
                        if lm_list[self.tip_ids[id]][2] < lm_list[self.tip_ids[id] - 2][2]:
                            fingers.append(1)
                        else:
                            fingers.append(0)
                    total = fingers.count(1)

                    text = ""
                    direction = mic.RCCAR(total)
                    if total == 0:
                        text = "BRAKE"

                    elif total == 5:
                        text = "FORWARD"

                    elif total == 2:
                        text = "RIGHT"

                    elif total == 3:
                        text = "LEFT"

                    elif total == 4:
                        text = "REVERSE"

                    cv2.putText(img, text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

            cv2.imshow("Hand Gesture Control", img)

            if cv2.waitKey(1) == 27:
                break

        self.cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    car_controller = CarController()
    car_controller.hand_gesture_control()