"""
Hand and Finger Schema Definition
"""

from typing import Tuple

import numpy as np
from pydantic import BaseModel

# Initialsing max and min measures referrence point
tmaxc = 0.4
tminc = 0.11

imaxc = 0.60
iminc = 0.24

mmaxc = 0.63
mminc = 0.13

rmaxc = 0.57
rminc = 0.14

lmaxc = 0.48
lminc = 0.18


class Finger(BaseModel):
    cmc: Tuple[float, float, float]
    mcp: Tuple[float, float, float]
    pip: Tuple[float, float, float]
    tip: Tuple[float, float, float]


class ActuatorData(BaseModel):
    thumb: int
    index: int
    middle: int
    ring: int
    little: int

    def to_list(self) -> Tuple[int, int, int, int, int]:
        return (self.thumb, self.index, self.middle, self.ring, self.little)


class Hand(BaseModel):
    wrist: Tuple[float, float, float]
    thumb: Finger
    index: Finger
    middle: Finger
    ring: Finger
    little: Finger

    def get_actuators(self) -> ActuatorData:
        T = int((np.linalg.norm(np.asarray(self.thumb.tip) - np.asarray(self.little.mcp))/(tmaxc-tminc))*100)-45
        I = int((np.linalg.norm(np.asarray(self.index.tip) - np.asarray(self.wrist))/(imaxc-iminc))*100)-62
        M = int((np.linalg.norm(np.asarray(self.middle.tip) - np.asarray(self.wrist))/(mmaxc-mminc))*100)-32
        R = int((np.linalg.norm(np.asarray(self.ring.tip) - np.asarray(self.wrist))/(rmaxc-rminc))*100)-29
        L = int((np.linalg.norm(np.asarray(self.little.tip) - np.asarray(self.wrist))/(lmaxc-lminc))*100)-58

        T = min(max(0, T), 100)
        I = min(max(0, I), 100)
        M = min(max(0, M), 100)
        R = min(max(0, R), 100)
        L = min(max(0, L), 100)

        return ActuatorData(
            thumb=T,
            index=I,
            middle=M,
            ring=R,
            little=L,
        )
        # thumb to pinky


def mediapipe_2_hand(hand_landmarks) -> Hand:
    """
    Covnerts mediapipe object to our Hand
    Refer to media/hand_landmarks.png
    """
    lms = [(0, 0, 0)] * 21
    for id, lm in enumerate(hand_landmarks.landmark):
        # Normalized landmarks in range [0.0, 1.0], relative to the image
        lms[id] = (lm.x, lm.y, lm.z)

    return Hand(
        wrist=lms[0],
        thumb=Finger(
            cmc=lms[1],
            mcp=lms[2],
            pip=lms[3],
            tip=lms[4],
        ),
        index=Finger(
            cmc=lms[5],
            mcp=lms[6],
            pip=lms[7],
            tip=lms[8],
        ),
        middle=Finger(
            cmc=lms[9],
            mcp=lms[10],
            pip=lms[11],
            tip=lms[12],
        ),
        ring=Finger(
            cmc=lms[13],
            mcp=lms[14],
            pip=lms[15],
            tip=lms[16],
        ),
        little=Finger(
            cmc=lms[17],
            mcp=lms[18],
            pip=lms[19],
            tip=lms[20],
        ),
    )
