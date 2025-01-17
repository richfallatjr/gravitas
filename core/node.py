import numpy as np
import random

class Node:
    def __init__(self, x=0, y=0, mass=1, velocity=None):
        self.position = np.array([x, y], dtype=float)
        self.velocity = np.array(velocity, dtype=float) if velocity is not None else np.zeros(2)
        self.mass = mass

class DynamicNode(Node):
    def __init__(self, mass=None, position=None, velocity=None):
        if position is None:
            position = np.random.uniform([100, 100], [700, 500])

        # 🌍 Balanced mass range for DNs
        if mass is None:
            mass = np.random.uniform(2.0, 8.0)  # Balanced range

        if velocity is None:
            velocity = np.random.uniform(-0.5, 0.5, size=2)

        super().__init__(position[0], position[1], mass, velocity)

        self.priority = 1 / self.mass
        self.trail = []

        # ✅ FIX: Initialize the proximity timer for merging behavior
        self.proximity_timer = 0

class PrimaryMassNode(Node):
    def __init__(self, x=None, y=None, mass=None, position=None, velocity=None):
        if position is not None:
            x, y = position
        elif x is None or y is None:
            x, y = np.random.uniform(100, 700), np.random.uniform(100, 500)

        # 🌌 Heavier but balanced PMNs
        if mass is None:
            mass = np.random.uniform(20.0, 40.0)

        if velocity is None:
            velocity = np.zeros(2)

        super().__init__(x, y, mass, velocity)
