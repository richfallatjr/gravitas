import numpy as np
from core.node import DynamicNode, PrimaryMassNode

class ForceCalculator:
    def apply_forces(self, nodes):
        G = 1.2
        softening = 5
        max_force = 15
        max_velocity = 20

        for node in nodes:
            if isinstance(node, DynamicNode):
                total_force = np.zeros(2)
                total_mass_weight = 0

                for other in nodes:
                    if isinstance(other, PrimaryMassNode):
                        r_vector = other.position - node.position
                        distance = np.linalg.norm(r_vector) + softening

                        # ✅ Gravitational Pull
                        force = (G * node.mass * other.mass) * r_vector / (distance ** 1.9)
                        total_force += force
                        total_mass_weight += other.mass / distance

                if total_mass_weight > 0:
                    averaged_force = total_force / total_mass_weight
                    force_magnitude = np.linalg.norm(averaged_force)
                    if force_magnitude > max_force:
                        averaged_force = (averaged_force / force_magnitude) * max_force

                    node.velocity += (averaged_force / node.mass) * 0.5

                # 🔄 Tangential motion
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
        for i, node_a in enumerate(nodes):
            if isinstance(node_a, DynamicNode):
                for j, node_b in enumerate(nodes):
                    if i >= j or not isinstance(node_b, DynamicNode):
                        continue  # Avoid double checks and self-collision

                    # ✅ Check for collision
                    r_vector = node_b.position - node_a.position
                    distance = np.linalg.norm(r_vector)
                    min_distance = 1.5 * ((node_a.mass ** (1/3)) + (node_b.mass ** (1/3)))
                    if distance < min_distance:
                        print(f"Collision detected between DN {i} and DN {j}")
                        self.elastic_collision(node_a, node_b)



                    if distance < min_distance:
                        # ✅ Apply elastic collision response
                        self.elastic_collision(node_a, node_b)


    def resolve_pmn_collisions(self, nodes):
        for i, node_a in enumerate(nodes):
            if isinstance(node_a, PrimaryMassNode):
                for j, node_b in enumerate(nodes):
                    if i >= j or not isinstance(node_b, PrimaryMassNode):
                        continue

                    # ✅ Check for collision
                    r_vector = node_b.position - node_a.position
                    distance = np.linalg.norm(r_vector)
                    min_distance = (node_a.mass ** (1/3)) + (node_b.mass ** (1/3))

                    if distance < min_distance:
                        # ✅ Elastic collision response
                        self.elastic_collision(node_a, node_b)

    def elastic_collision(self, node_a, node_b):
        # ✅ Compute the normal vector between the nodes
        normal_vector = node_b.position - node_a.position
        distance = np.linalg.norm(normal_vector)

        if distance == 0:
            # Prevent division by zero by adding a small random nudge
            normal_vector = np.random.rand(2) - 0.5
            distance = np.linalg.norm(normal_vector)

        normal_vector /= distance

        # ✅ Push overlapping nodes apart slightly
        overlap = 0.5 * ((node_a.mass ** (1/3)) + (node_b.mass ** (1/3))) - distance
        if overlap > 0:
            correction = normal_vector * overlap
            node_a.position -= correction * (node_b.mass / (node_a.mass + node_b.mass))
            node_b.position += correction * (node_a.mass / (node_a.mass + node_b.mass))

        # ✅ Relative velocity
        relative_velocity = node_a.velocity - node_b.velocity
        velocity_along_normal = np.dot(relative_velocity, normal_vector)

        if velocity_along_normal > 0:
            return  # Nodes are moving apart, no need to resolve

        # ✅ Compute impulse scalar
        restitution = 0.9  # Elasticity: 1.0 is perfectly elastic, <1.0 is inelastic
        impulse_magnitude = -(1 + restitution) * velocity_along_normal
        impulse_magnitude /= (1 / node_a.mass) + (1 / node_b.mass)

        # ✅ Apply the impulse to the velocities
        impulse = impulse_magnitude * normal_vector
        node_a.velocity += impulse / node_a.mass
        node_b.velocity -= impulse / node_b.mass

        # ✅ Optional: Slight damping to stabilize bouncing
        node_a.velocity *= 0.98
        node_b.velocity *= 0.98


