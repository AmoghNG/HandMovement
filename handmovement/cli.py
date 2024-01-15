"""CLI interface for handmovement project.

Takes camera input, finds the right hand and sends actuator
commands to the arduino via serial
"""

import time

import cv2
import mediapipe as mp
import numpy as np

from handmovement.arduino import SerialInterface
from handmovement.schema import ActuatorData, mediapipe_2_hand


def main():  # pragma: no cover
    """
    The main function executes on commands:
    `python -m handmovement` and `$ handmovement `.

    This is your program's entry point.


    """

    arduino = SerialInterface(
        port="COM5",
        baudrate=115200,
    )

    for i in range(0, 100, 1):
        dummy_data = ActuatorData(thumb=i, index=i, middle=i, ring=i, little=i)
        arduino.send_actuator_percs(dummy_data, wait_for_ack=True)
        time.sleep(0.1)

    mp_drawing = mp.solutions.drawing_utils
    mp_hands = mp.solutions.hands

    old_actuator_data = [0, 0, 0, 0, 0]
    # For webcam input:
    cap = cv2.VideoCapture(0)
    with mp_hands.Hands(
        min_detection_confidence=0.5, min_tracking_confidence=0.5
    ) as hands:
        while cap.isOpened():
            success, image = cap.read()
            if not success:
                print("Ignoring empty camera frame.")
                # If loading a video, use 'break' instead of 'continue'.
                continue

            # Flip the image horizontally for a later
            # selfie-view display, and convert
            # the BGR image to RGB.
            image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
            # To improve performance, optionally mark the image
            # as not writeable to pass by reference.
            image.flags.writeable = False
            results = hands.process(image)

            # Draw the hand annotations on the image.
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            if results.multi_hand_landmarks:
                for index, hand_landmarks in enumerate(
                    results.multi_hand_landmarks
                ):
                    hand_label = (
                        results.multi_handedness[index].classification[0].label
                    )
                    if hand_label != "Right":
                        # Skip if not right hand
                        continue

                    mp_drawing.draw_landmarks(
                        image, hand_landmarks, mp_hands.HAND_CONNECTIONS
                    )

                    hand = mediapipe_2_hand(hand_landmarks)
                    actuator_percs = hand.get_actuators()
                    actuator_data = actuator_percs.to_list()

                    vis_hand = map(
                        lambda x: str(x).zfill(3) + "%", actuator_data
                    )
                    vis_hand = " ".join(vis_hand)

                    # Add vis_hand text to the image
                    cv2.putText(
                        image,
                        vis_hand,
                        (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (255, 255, 255),
                        2,
                        cv2.LINE_AA,
                    )

                    # Compare old_actuator_data and actuator_data
                    # Only if there is significant change, proceed to send data
                    if (
                        actuator_data != old_actuator_data
                        and (
                            abs(
                                np.asarray(actuator_data)
                                - np.asarray(old_actuator_data)
                            )
                            > 5
                        ).any()
                    ):
                        old_actuator_data = actuator_data

                        arduino.send_actuator_percs(
                            actuator_data=actuator_percs, wait_for_ack=True
                        )

            cv2.imshow("MediaPipe Hands", image)
            key = cv2.waitKey(1)
            if key == ord("q"):
                break
    cap.release()
