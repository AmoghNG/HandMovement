"""
Hand and Finger Schema Definition
"""

from typing import Tuple

import numpy as np
from pydantic import BaseModel

# Initialsing max and min measures referrence point
tmaxc = 15.5
tminc = 0
trmeasure = 3


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
        tsc = (
            np.linalg.norm(
                np.asarray(self.thumb.tip) - np.asarray(self.thumb.pip)
            )
            / trmeasure
        )
        tma = tmaxc * tsc
        tmi = tminc * tsc
        tpercent = (
            (
                np.linalg.norm(
                    np.asarray(self.thumb.tip) - np.asarray(self.little.mcp)
                )
                - tmi
            )
            / tma
        ) * 100
        tpercent_int = int(tpercent)
        return ActuatorData(
            thumb=tpercent_int,
            index=0,
            middle=0,
            ring=0,
            little=0,
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
