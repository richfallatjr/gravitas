# core/simulation_controller.py

from ui.main_window import MainWindow
from core.force_calculator import ForceCalculator
from core.motion_integrator import MotionIntegrator
from core.collision_handler import CollisionHandler
from core.node import DynamicNode, PrimaryMassNode
from PyQt5.QtWidgets import QApplication
import numpy as np
import sys

# Constants for merging behavior
PROXIMITY_THRESHOLD = 20  # Distance in pixels for merging
MERGE_TIME_THRESHOLD = 50  # Frames required to trigger merging

class SimulationController:
    def __init__(self):
        self.force_calculator = ForceCalculator()
        self.motion_integrator = MotionIntegrator()
        self.collision_handler = CollisionHandler()
        self.nodes = []
        self.enable_dn_collisions = False  # ✅ Default: Collisions are ON
        self.setup_simulation()

    def setup_simulation(self):
        # ✅ Initialize multiple PMNs at different positions
        self.nodes.append(PrimaryMassNode(200, 150, 50))
        self.nodes.append(PrimaryMassNode(600, 150, 50))
        self.nodes.append(PrimaryMassNode(400, 450, 50))

        # ✅ Initialize multiple DNs
        for _ in range(50):
            self.nodes.append(DynamicNode())

    def update(self):
        # ✅ Apply forces and update positions
        self.force_calculator.apply_forces(self.nodes)
        # ✅ Check for PMN collisions
        self.force_calculator.resolve_pmn_collisions(self.nodes)
        # ✅ Apply DN collisions only if enabled
        if self.enable_dn_collisions:
            self.force_calculator.resolve_dn_collisions(self.nodes)
            
        self.motion_integrator.update_positions(self.nodes)

        # ✅ Check for merging behavior
        self.check_proximity_and_merge()

        # ✅ Refresh the UI
        if self.window and hasattr(self.window, 'simulation_view'):
            self.window.simulation_view.update()

    def check_proximity_and_merge(self):
        for node in self.nodes[:]:
            if isinstance(node, DynamicNode):
                closest_pmn = self.find_closest_pmn(node)
                if closest_pmn:
                    distance = np.linalg.norm(closest_pmn.position - node.position)

                    if distance < PROXIMITY_THRESHOLD:
                        node.proximity_timer += 1

                        if node.proximity_timer >= MERGE_TIME_THRESHOLD:
                            # 💥 Trigger particle burst on absorption
                            self.trigger_particle_burst(closest_pmn.position)

                            # 💥 Merge: Add DN mass to PMN
                            closest_pmn.mass += node.mass
                            self.nodes.remove(node)
                            print(f"[Merge] DN merged into PMN. PMN mass: {closest_pmn.mass}")
                    else:
                        node.proximity_timer = 0

    def trigger_particle_burst(self, position):
        # 💥 Simple burst: Spawn small particles flying outward
        for _ in range(10):
            angle = np.random.uniform(0, 2 * np.pi)
            speed = np.random.uniform(0.5, 2.0)
            velocity = np.array([np.cos(angle), np.sin(angle)]) * speed

            # Create a small, fast-moving node as a particle effect
            burst_particle = DynamicNode(mass=0.1, position=position, velocity=velocity)
            burst_particle.lifetime = 15  # Particles disappear after a short time
            self.nodes.append(burst_particle)

    def find_closest_pmn(self, dynamic_node):
        # ✅ Find the closest PMN to a given DN
        pmns = [n for n in self.nodes if isinstance(n, PrimaryMassNode)]
        if not pmns:
            return None

        return min(pmns, key=lambda pmn: np.linalg.norm(pmn.position - dynamic_node.position))

    def run(self):
        app = QApplication(sys.argv)
        self.window = MainWindow(self)
        self.window.show()
        sys.exit(app.exec_())
