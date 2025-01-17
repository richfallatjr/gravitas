# core/node.py
import numpy as np

class Node:
    def __init__(self, x=0, y=0, mass=1):
        self.position = np.array([x, y], dtype=float)
        self.velocity = np.zeros(2)
        self.mass = mass

class DynamicNode(Node):
    def __init__(self):
        super().__init__(np.random.uniform(100, 700), np.random.uniform(100, 500), 1)

class PrimaryMassNode(Node):
    def __init__(self, x, y, mass):
        super().__init__(x, y, mass)