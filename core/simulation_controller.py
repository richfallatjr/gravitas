from ui.main_window import MainWindow
from core.force_calculator import ForceCalculator
from core.motion_integrator import MotionIntegrator
from core.node import DynamicNode, PrimaryMassNode
from PyQt5.QtWidgets import QApplication
import numpy as np
import sys
import json

# Constants for merging behavior (can be dynamically loaded)
DEFAULT_PROXIMITY_THRESHOLD = 20  # Distance in pixels for merging
DEFAULT_MERGE_TIME_THRESHOLD = 50  # Frames required to trigger merging


class SimulationController:
    def __init__(self, config_file="data/config.json", dn_file="data/dn_dataset.json", pmn_file="data/pmn_dataset.json"):
        self.force_calculator = ForceCalculator()
        self.motion_integrator = MotionIntegrator()
        self.nodes = []
        self.enable_dn_collisions = False  # ✅ Default: Collisions are OFF
        self.config = self.load_config(config_file)
        self.setup_simulation(dn_file, pmn_file)

    def load_config(self, config_file):
        """
        Load the global configuration file for system-wide parameters.
        """
        try:
            with open(config_file, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"[Warning] Config file not found: {config_file}. Using defaults.")
            return {
                "proximity_threshold": DEFAULT_PROXIMITY_THRESHOLD,
                "merge_time_threshold": DEFAULT_MERGE_TIME_THRESHOLD,
            }

    def setup_simulation(self, dn_file, pmn_file):
        """
        Initialize the simulation with nodes loaded from JSON datasets.
        """
        self.load_pmns(pmn_file)
        self.load_dns(dn_file)

    def load_pmns(self, pmn_file):
        """
        Load PrimaryMassNodes from the PMN dataset file.
        """
        try:
            with open(pmn_file, "r") as file:
                pmns = json.load(file)
            for pmn_data in pmns:
                # Ensure unique positions for PMNs
                position = self.get_unique_position(existing_positions=[
                    pmn.position for pmn in self.nodes if isinstance(pmn, PrimaryMassNode)
                ])
                self.nodes.append(PrimaryMassNode(position=position, **pmn_data))
        except FileNotFoundError:
            print(f"[Warning] PMN dataset file not found: {pmn_file}")

    def get_unique_position(self, existing_positions, min_distance=50):
        """
        Generate a unique position for a node, ensuring minimum separation from existing positions.
        """
        while True:
            position = np.random.uniform([100, 100], [700, 500])
            if all(np.linalg.norm(position - np.array(p)) > min_distance for p in existing_positions):
                return position


    def load_dns(self, dn_file):
        """
        Load DynamicNodes from the DN dataset file.
        """
        try:
            with open(dn_file, "r") as file:
                dns = json.load(file)
            for dn_data in dns:
                attributes = dn_data.get("attributes", {})
                self.nodes.append(DynamicNode(attributes=attributes))
        except FileNotFoundError:
            print(f"[Warning] DN dataset file not found: {dn_file}")

    def update(self):
        """
        Update the simulation: apply forces, update positions, resolve collisions, and handle merging.
        """
        # Apply forces and update positions
        self.force_calculator.apply_forces(self.nodes)
        self.force_calculator.resolve_pmn_collisions(self.nodes)

        if self.enable_dn_collisions:
            self.force_calculator.resolve_dn_collisions(self.nodes)

        self.motion_integrator.update_positions(self.nodes)

        # Check for merging behavior
        self.check_proximity_and_merge()

        # Refresh the UI
        if self.window and hasattr(self.window, 'simulation_view'):
            self.window.simulation_view.update()

    def check_proximity_and_merge(self):
        """
        Check proximity between DNs and PMNs, and merge DNs into PMNs if thresholds are met.
        """
        proximity_threshold = self.config.get("proximity_threshold", DEFAULT_PROXIMITY_THRESHOLD)
        merge_time_threshold = self.config.get("merge_time_threshold", DEFAULT_MERGE_TIME_THRESHOLD)

        for node in self.nodes[:]:
            if isinstance(node, DynamicNode):
                closest_pmn = self.find_closest_pmn(node)
                if closest_pmn:
                    distance = np.linalg.norm(closest_pmn.position - node.position)
                    if distance < proximity_threshold:
                        node.proximity_timer += 1
                        if node.proximity_timer >= merge_time_threshold:
                            self.merge_dn_into_pmn(node, closest_pmn)
                    else:
                        node.proximity_timer = 0

    def merge_dn_into_pmn(self, dn, pmn):
        """
        Merge a DynamicNode into a PrimaryMassNode.
        """
        pmn.mass += dn.mass  # Add DN mass to PMN
        self.trigger_particle_burst(pmn.position)  # Visual effect
        self.nodes.remove(dn)
        print(f"[Merge] DN absorbed by PMN. New PMN mass: {pmn.mass}")

    def trigger_particle_burst(self, position):
        """
        Create a particle burst effect at the given position.
        """
        particle_count = 10
        for _ in range(particle_count):
            angle = np.random.uniform(0, 2 * np.pi)
            speed = np.random.uniform(0.5, 2.0)
            velocity = np.array([np.cos(angle), np.sin(angle)]) * speed
            burst_particle = DynamicNode(mass=0.1, position=position, velocity=velocity)
            burst_particle.lifetime = 15  # Particles disappear after a short time
            self.nodes.append(burst_particle)

    def find_closest_pmn(self, dynamic_node):
        """
        Find the closest PMN to a given DN.
        """
        pmns = [n for n in self.nodes if isinstance(n, PrimaryMassNode)]
        return min(pmns, key=lambda pmn: np.linalg.norm(pmn.position - dynamic_node.position), default=None)

    def run(self):
        """
        Run the simulation.
        """
        app = QApplication(sys.argv)
        self.window = MainWindow(self)
        self.window.show()
        sys.exit(app.exec_())
