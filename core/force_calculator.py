from core.node import DynamicNode, PrimaryMassNode
import numpy as np

class ForceCalculator:
    def apply_forces(self, nodes):
        G = 9  # ✅ Moderate gravity to avoid being too sticky
        softening = 2  # ✅ Prevents extreme forces up close
        max_force = 50  # ✅ Allow stronger force bursts without overwhelming

        for node in nodes:
            if isinstance(node, DynamicNode):
                total_force = np.zeros(2)

                for other in nodes:
                    if isinstance(other, PrimaryMassNode):
                        r_vector = other.position - node.position
                        distance = np.linalg.norm(r_vector) + softening

                        # ✅ Gravity weakens closer in, stronger farther out (dynamic scaling)
                        distance_factor = np.clip(distance / 200, 0.5, 2.0)
                        force_magnitude = G * other.mass * node.mass / (distance**2) * distance_factor
                        force_magnitude = min(force_magnitude, max_force)

                        force_direction = r_vector / distance
                        force = force_direction * force_magnitude
                        total_force += force

                        # ✅ Stronger tangential motion for slingshot effect
                        tangent = np.array([-r_vector[1], r_vector[0]])
                        norm = np.linalg.norm(tangent)
                        if norm != 0:
                            tangent /= norm
                            node.velocity += tangent * 0.002  # ⬆️ Stronger tangential injection

                # ✅ Apply adjusted force and allow stronger accelerations
                acceleration = total_force / node.mass
                node.velocity += acceleration * 1  # ⬆️ More aggressive force application

                # ✅ Lower damping to retain speed
                node.velocity *= 0.995  # ⬆️ Less damping = more speed retention

                # 🌠 Occasional random kicks for chaos
                if np.random.rand() < 0.02:
                    random_push = (np.random.rand(2) - 0.5) * 0.5
                    node.velocity += random_push
