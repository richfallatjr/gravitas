import numpy as np
import random

class Node:
    def __init__(self, x=0, y=0, mass=1, velocity=None):
        self.position = np.array([x, y], dtype=float)
        self.velocity = np.array(velocity, dtype=float) if velocity is not None else np.zeros(2)
        self.mass = mass


class DynamicNode(Node):
    def __init__(self, mass=None, attributes=None, position=None, velocity=None):
        """
        DynamicNode represents a task or item with configurable attributes.

        :param mass: Explicit mass (optional, overrides attributes-based calculation).
        :param attributes: Dictionary containing DN attributes (e.g., threads, memory, render_time).
        :param position: Initial position as a 2D array. Random if None.
        :param velocity: Initial velocity as a 2D array. Random if None.
        """
        if attributes is None:
            attributes = {"threads": np.random.randint(2, 16), "memory": np.random.randint(1024, 8192), "render_time": np.random.uniform(1, 10)}
        self.attributes = attributes

        if position is None:
            position = np.random.uniform([100, 100], [700, 500])

        if velocity is None:
            velocity = np.random.uniform(-0.5, 0.5, size=2)

        # Use the provided mass or calculate it from attributes
        self.mass = mass if mass is not None else self.calculate_mass()

        super().__init__(position[0], position[1], self.mass, velocity)

        self.priority = 1 / self.mass
        self.trail = []
        self.proximity_timer = 0

    def calculate_mass(self):
        """
        Calculate the mass of the DN based on its attributes.
        """
        return self.attributes.get("render_time", 1)  # Default mass proxy



class PrimaryMassNode(Node):
    def __init__(self, x=None, y=None, mass=None, position=None, velocity=None, **kwargs):
        """
        Initialize a PrimaryMassNode with attributes such as threads, memory, etc.

        :param x: X-coordinate of the node.
        :param y: Y-coordinate of the node.
        :param mass: Mass of the node (calculated if not provided).
        :param position: 2D position array (overrides x, y if provided).
        :param velocity: Initial velocity (default is stationary).
        :param kwargs: Additional attributes like threads, memory, chipset_speed.
        """
        self.threads = kwargs.get("threads", 16)  # Default threads
        self.memory = kwargs.get("memory", 8192)  # Default memory
        self.chipset_speed = kwargs.get("chipset_speed", "2.0GHz")
        self.preferences = kwargs.get("preferences", {})

        # Set position
        if position is not None:
            x, y = position
        elif x is None or y is None:
            x, y = np.random.uniform(100, 700), np.random.uniform(100, 500)

        # Calculate mass based on threads if not explicitly provided
        if mass is None:
            mass = self.calculate_mass()

        # Default velocity is stationary
        if velocity is None:
            velocity = np.zeros(2)

        super().__init__(x, y, mass, velocity)

    def calculate_mass(self):
        """
        Calculate the mass of the PMN based on threads.
        """
        return self.threads  # Use threads as a proxy for mass

