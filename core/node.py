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
            attributes = {
                "threads": np.random.randint(2, 16),
                "memory": np.random.randint(1024, 8192),
                "render_time": np.random.uniform(1, 10)
            }
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
    id_counter = 0  # Static counter for unique IDs

    def __init__(self, x=None, y=None, mass=None, position=None, velocity=None, **attributes):
        if position is not None:
            x, y = position
        elif x is None or y is None:
            x, y = np.random.uniform(100, 700), np.random.uniform(100, 500)

        # Heavier but balanced PMNs
        if mass is None:
            mass = np.random.uniform(20.0, 40.0)

        if velocity is None:
            velocity = np.zeros(2)

        super().__init__(x, y, mass, velocity)

        self.id = PrimaryMassNode.id_counter  # Assign a unique ID
        PrimaryMassNode.id_counter += 1

        self.attributes = attributes or {}
        self.threads = self.attributes.get("threads", 1)  # Extract threads
        self.memory = self.attributes.get("memory", 1024)  # Extract memory
        self.preferences = self.attributes.get("preferences", {})  # Extract preferences
        self.current_dns = []  # Tracks currently processing DNs
        self.idle_timer = 0  # Tracks idle time
        self.processing_capacity = 0  # Tracks processing load

    def can_process_more(self):
        """
        Determine if the PMN can process more DNs based on available threads.
        """
        current_threads_used = sum(dn.attributes.get("threads", 1) for dn, _ in self.current_dns)
        return current_threads_used < self.threads  # Only allow if threads are available

    def update_processing_capacity(self):
        """
        Update the processing capacity based on the current load (active DNs).
        """
        total_mass = sum(dn.mass for dn, _ in self.current_dns)
        self.processing_capacity = min(total_mass / self.mass, 1.0)  # Ensure capacity is clamped to 1.0
