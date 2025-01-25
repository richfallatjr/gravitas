import numpy as np
import random

class Node:
    def __init__(self, x=0, y=0, mass=1, velocity=None):
        self.position = np.array([x, y], dtype=float)
        self.velocity = np.array(velocity, dtype=float) if velocity is not None else np.zeros(2)
        self.mass = mass


class DynamicNode(Node):
    def __init__(self, mass=None, config=None, attributes=None, position=None, velocity=None):
        """
        DynamicNode represents a task or item with configurable attributes.

        :param config: Configuration for normalization and weights.
        :param attributes: Dictionary containing DN attributes (e.g., threads, memory, render_time).
        :param position: Initial position as a 2D array. Random if None.
        :param velocity: Initial velocity as a 2D array. Random if None.
        """
        self.config = config or {}
        self.attributes = attributes or {}

        # Default random attributes if not provided
        if not self.attributes:
            self.attributes = {
                "render_time": np.random.uniform(1, 10),
                "memory": np.random.uniform(1024, 8192),
                "threads": np.random.randint(1, 16)
            }

        if not mass:
            # Calculate mass using the config
            self.mass = self.calculate_mass()
        else:
            self.mass = mass

        # Randomize position and velocity if not provided
        if position is None:
            position = np.random.uniform([100, 100], [700, 500])

        if velocity is None:
            velocity = np.random.uniform(-0.5, 0.5, size=2)

        # Call the parent class initializer
        super().__init__(position[0], position[1], self.mass, velocity)

        # Initialize the trail attribute
        self.trail = []  # List to store the history of positions

    def calculate_mass(self):
        """
        Calculate the mass of the DN based on attributes and config weights.
        Includes a base mass and amplified scaling to avoid extremely small values.
        """
        total_weight = sum(v["weight"] for v in self.config.get("attributes", {}).values())
        base_mass = 1  # Ensure every DN has at least this mass
        mass = 0.0

        for attr, settings in self.config.get("attributes", {}).items():
            value = self.attributes.get(attr, 0)  # Attribute value

            # Normalize only if min and max are set
            if "min" in settings and "max" in settings:
                normalized = (value - settings["min"]) / (settings["max"] - settings["min"])
                normalized = max(0, min(1, normalized))  # Clamp between 0 and 1
            else:
                normalized = value  # Use raw value if no normalization range

            mass += normalized * settings["weight"]

        # Amplify mass scaling and add base mass
        scaled_mass = base_mass + (mass / max(1.0, total_weight) * 10.0)

        # Clamp mass to avoid extremes
        return max(5, min(scaled_mass, 100))  # Clamp between 5 and 100






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
