from core.node import DynamicNode, PrimaryMassNode
import numpy as np

class ForceCalculator:
    def apply_forces(self, nodes):
        G = 5  # 🔥 Increased gravitational constant for stronger pull
        softening = 1  # 🔥 Reduced softening for more realistic gravity

        for node in nodes:
            if isinstance(node, DynamicNode):
                force = np.zeros(2)
                for other in nodes:
                    if isinstance(other, PrimaryMassNode):
                        r_vector = other.position - node.position
                        distance = np.linalg.norm(r_vector) + softening

                        # ✅ Stronger gravitational pull
                        force += G * other.mass * r_vector / distance**3

                        # ✅ Reduced tangential kick for tighter orbits
                        tangent = np.array([-r_vector[1], r_vector[0]])
                        tangent /= np.linalg.norm(tangent)
                        node.velocity += tangent * 0.005  # 🔥 Reduced kick

                # ✅ Apply the stronger gravitational force
                node.velocity += force * 0.1  # 🔥 Stronger force application

                # ✅ Slight damping to prevent runaway velocities
                node.velocity *= 0.995
