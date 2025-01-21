import numpy as np
from core.node import DynamicNode, PrimaryMassNode
import json

class ForceCalculator:
    def __init__(self, config):
        #self.config = config
        
        with open(config, "r") as file:
            self.config = json.load(file)
        
    def apply_forces(self, nodes):
        """
        Calculate gravitational forces between DNs and PMNs and update velocities.
        """
        G = 1.2  # Gravitational constant (scaling factor)
        softening = 5
        max_force = 15
        max_velocity = 20

        for node in nodes:
            if isinstance(node, DynamicNode):
                total_force = np.zeros(2)

                for other in nodes:
                    if isinstance(other, PrimaryMassNode):
                        # Calculate per-PMN gravitational charge
                        gravitational_charge = self.calculate_gravitational_charge(node, other)

                        # Compute distance and force
                        r_vector = other.position - node.position
                        distance = np.linalg.norm(r_vector) + softening
                        force = (G * gravitational_charge) * r_vector / (distance ** 1.9)

                        total_force += force

                # Apply force to the DN
                force_magnitude = np.linalg.norm(total_force)
                if force_magnitude > max_force:
                    total_force = (total_force / force_magnitude) * max_force

                node.velocity += (total_force / node.mass) * 100

                # Apply tangential motion and random perturbations
                self.apply_perturbations(node, max_velocity)

    def calculate_gravitational_charge(self, dn, pmn):
        """
        Calculate the gravitational charge for a DynamicNode (DN) relative to a PrimaryMassNode (PMN).
        The gravitational charge is based on the DN's attributes and the PMN's preferences.
        """
        charge = 0.0
        preferences = pmn.attributes.get("preferences", {})  # Safely get preferences from PMN attributes
        config_attributes = self.config.get("attributes", {})
        invert_attributes = self.config.get("invert_attributes", [])

        for attribute, weight in preferences.items():
            # Retrieve DN attribute value and default to 0 if not found
            dn_value = dn.attributes.get(attribute, 0)
            attr_config = config_attributes.get(attribute, {})

            # Normalize attribute value if min and max are available in the config
            min_value = attr_config.get("min", 0)
            max_value = attr_config.get("max", 1)  # Avoid divide-by-zero with a sensible default
            if max_value != min_value:
                dn_value = (dn_value - min_value) / (max_value - min_value)

            # Apply inversion if the attribute is listed in invert_attributes
            if attribute in invert_attributes:
                dn_value = 1.0 - dn_value

            # Accumulate the charge
            charge += weight * dn_value

        return charge


    def apply_perturbations(self, node, max_velocity):
        """
        Apply tangential motion, random micro-perturbations, and clamp velocity.
        """
        # Tangential motion
        tangent_vector = np.array([-node.velocity[1], node.velocity[0]])
        tangent_norm = np.linalg.norm(tangent_vector)
        if tangent_norm != 0:
            tangent_vector /= tangent_norm
            node.velocity += tangent_vector * np.random.uniform(0.005, 0.01)

        # Random micro-perturbation
        random_nudge = (np.random.rand(2) - 0.5) * 0.2
        node.velocity += random_nudge

        # Clamp velocity
        speed = np.linalg.norm(node.velocity)
        if speed > max_velocity:
            node.velocity = (node.velocity / speed) * max_velocity

        # Damping
        node.velocity *= 0.998

    def resolve_dn_collisions(self, nodes):
        """
        Resolve collisions between DNs.
        """
        for i, node_a in enumerate(nodes):
            if isinstance(node_a, DynamicNode):
                for j, node_b in enumerate(nodes):
                    if i >= j or not isinstance(node_b, DynamicNode):
                        continue

                    r_vector = node_b.position - node_a.position
                    distance = np.linalg.norm(r_vector)
                    min_distance = 1.5 * ((node_a.mass ** (1/3)) + (node_b.mass ** (1/3)))

                    if distance < min_distance:
                        self.elastic_collision(node_a, node_b)

    def resolve_pmn_collisions(self, nodes):
        """
        Resolve collisions between PMNs.
        """
        for i, node_a in enumerate(nodes):
            if isinstance(node_a, PrimaryMassNode):
                for j, node_b in enumerate(nodes):
                    if i >= j or not isinstance(node_b, PrimaryMassNode):
                        continue

                    r_vector = node_b.position - node_a.position
                    distance = np.linalg.norm(r_vector)
                    min_distance = (node_a.mass ** (1/3)) + (node_b.mass ** (1/3))

                    if distance < min_distance:
                        self.elastic_collision(node_a, node_b)

    def elastic_collision(self, node_a, node_b):
        """
        Resolve elastic collisions between two nodes.
        """
        normal_vector = node_b.position - node_a.position
        distance = np.linalg.norm(normal_vector)

        if distance == 0:
            normal_vector = np.random.rand(2) - 0.5
            distance = np.linalg.norm(normal_vector)

        normal_vector /= distance
        overlap = 0.5 * ((node_a.mass ** (1/3)) + (node_b.mass ** (1/3))) - distance
        if overlap > 0:
            correction = normal_vector * overlap
            node_a.position -= correction * (node_b.mass / (node_a.mass + node_b.mass))
            node_b.position += correction * (node_a.mass / (node_a.mass + node_b.mass))

        relative_velocity = node_a.velocity - node_b.velocity
        velocity_along_normal = np.dot(relative_velocity, normal_vector)

        if velocity_along_normal > 0:
            return

        restitution = 0.9
        impulse_magnitude = -(1 + restitution) * velocity_along_normal
        impulse_magnitude /= (1 / node_a.mass) + (1 / node_b.mass)

        impulse = impulse_magnitude * normal_vector
        node_a.velocity += impulse / node_a.mass
        node_b.velocity -= impulse / node_b.mass

        node_a.velocity *= 0.98
        node_b.velocity *= 0.98
