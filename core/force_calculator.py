from core.node import DynamicNode, PrimaryMassNode
import numpy as np

class ForceCalculator:
    def apply_forces(self, nodes):
        G = 1.2  # 🔥 Boosted gravity to enhance attraction
        softening = 5  # 🛡️ Prevents division by zero
        max_force = 15  # 🚀 Higher force cap to allow stronger pulls
        max_velocity = 20  # 🚀 Higher velocity cap for slingshots

        for node in nodes:
            if isinstance(node, DynamicNode):
                total_force = np.zeros(2)
                total_mass_weight = 0

                for other in nodes:
                    if isinstance(other, PrimaryMassNode):
                        r_vector = other.position - node.position
                        distance = np.linalg.norm(r_vector) + softening

                        # ✅ Stronger gravitational pull with softer falloff
                        force = (G * node.mass * other.mass) * r_vector / (distance ** 1.9)

                        # ✅ Force averaging
                        total_force += force
                        total_mass_weight += other.mass / distance

                # ✅ Apply averaged force
                if total_mass_weight > 0:
                    averaged_force = total_force / total_mass_weight

                    # 🔒 Clamp force for safety
                    force_magnitude = np.linalg.norm(averaged_force)
                    if force_magnitude > max_force:
                        averaged_force = (averaged_force / force_magnitude) * max_force

                    # ✅ Apply the stronger force
                    node.velocity += (averaged_force / node.mass) * 0.5

                # ✅ Stronger tangential motion for slingshots
                tangent_vector = np.array([-node.velocity[1], node.velocity[0]])
                tangent_norm = np.linalg.norm(tangent_vector)
                if tangent_norm != 0:
                    tangent_vector /= tangent_norm
                    node.velocity += tangent_vector * np.random.uniform(0.005, 0.01)  # 🚀 Stronger orbital push

                # ✅ Random micro-perturbations to disrupt balance
                random_nudge = (np.random.rand(2) - 0.5) * 0.2
                node.velocity += random_nudge

                # 🔒 Clamp velocity to allow escape but prevent chaos
                speed = np.linalg.norm(node.velocity)
                if speed > max_velocity:
                    node.velocity = (node.velocity / speed) * max_velocity

                # 🔧 Reduce damping for more energetic movement
                node.velocity *= 0.998
