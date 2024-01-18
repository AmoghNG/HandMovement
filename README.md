# Biomimicry with Nitinol: Using Nickel-Titanium alloy wire’s shape memory effect to simulate organic muscles

[![CI](https://github.com/AmoghNG/HandMovement/actions/workflows/main.yml/badge.svg)](https://github.com/AmoghNG/HandMovement/actions/workflows/main.yml)

Hand Movement created by AmoghNG

Make use of the Mediapipe Hand Tracking module to track hand movements and actuate a robot arm. This repository in an implementation of the software and hardware platform for the paper.

<b>Abstract</b>: This paper explores how to use nickel-titanium (nitinol) wires to replicate organic movement in robots. Nitinol wires have an interesting feature: they can return to their original shape when heated or provided electricity. This is called the shape memory effect. By using this effect, this paper aims to create "mechanical muscles" that act like real muscles, contracting and relaxing to move parts of a robot. This is important because making robots move naturally is challenging, something known as Moravec's Paradox [1]. It tells us that things humans do without thinking, like moving and sensing the world, are actually really hard for robots. A design idea known as biomimicry is being used, which means we look at how the human body works and try to copy that in robots. Humans have a complex system of muscles and nerves that work together seamlessly, and we want our robots to do the same. If we can accurately figure out how nitinol wires work and apply that knowledge, we might make robots move as smoothly and efficiently as humans do. This research could help us make big leaps in how we design and understand robots, bringing them closer to natural human movement.	


## Usage

```bash
$ python -m handmovement
```

## Development

Read the [CONTRIBUTING.md](CONTRIBUTING.md) file.


## Mediapipe Hand Representation

<img src="media/hand_landmarks.png">

We make use of the Mediapipe hand 3D representation
