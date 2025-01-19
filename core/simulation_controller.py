from ui.main_window import MainWindow
from core.force_calculator import ForceCalculator
from core.motion_integrator import MotionIntegrator
from core.node import DynamicNode, PrimaryMassNode
from PyQt5.QtWidgets import QApplication
import numpy as np
import sys
import json

DEFAULT_PROXIMITY_THRESHOLD = 20  # Distance in pixels for merging
DEFAULT_MERGE_TIME_THRESHOLD = 50  # Frames required to trigger merging


class SimulationController:
    def __init__(self, config_file="data/config.json", dn_file="data/dn_dataset.json", pmn_file="data/pmn_dataset.json"):
        self.force_calculator = ForceCalculator()
        self.motion_integrator = MotionIntegrator()
        self.nodes = []
        self.enable_dn_collisions = False  # Default: Collisions are OFF
        self.config = self.load_config(config_file)
        self.setup_simulation(dn_file, pmn_file)
        self.tick_counter = 0  # Add a tick counter for throttling

    def load_config(self, config_file):
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
        self.load_pmns(pmn_file)
        self.load_dns(dn_file)

    def load_pmns(self, pmn_file):
        try:
            with open(pmn_file, "r") as file:
                pmns = json.load(file)
            for pmn_data in pmns:
                position = self.get_unique_position(existing_positions=[
                    pmn.position for pmn in self.nodes if isinstance(pmn, PrimaryMassNode)
                ])
                self.nodes.append(PrimaryMassNode(position=position, **pmn_data))
        except FileNotFoundError:
            print(f"[Warning] PMN dataset file not found: {pmn_file}")

    def get_unique_position(self, existing_positions, min_distance=50):
        while True:
            position = np.random.uniform([100, 100], [700, 500])
            if all(np.linalg.norm(position - np.array(p)) > min_distance for p in existing_positions):
                return position

    def load_dns(self, dn_file):
        try:
            with open(dn_file, "r") as file:
                dns = json.load(file)
            for dn_data in dns:
                attributes = dn_data.get("attributes", {})
                self.nodes.append(DynamicNode(attributes=attributes))
        except FileNotFoundError:
            print(f"[Warning] DN dataset file not found: {dn_file}")

    def update(self):
        self.force_calculator.apply_forces(self.nodes)
        self.motion_integrator.update_positions(self.nodes)

        if self.enable_dn_collisions:
            self.force_calculator.resolve_dn_collisions(self.nodes)

        self.simulate_processing()

        if self.window and hasattr(self.window, 'simulation_view'):
            self.window.simulation_view.update()

    def simulate_processing(self):
        for pmn in [node for node in self.nodes if isinstance(node, PrimaryMassNode)]:
            pmn.update_processing_capacity()

            print(f"[Processing] PMN {pmn} - Capacity: {pmn.processing_capacity:.2f}")

            completed_dns = []
            for i, (dn, time_left) in enumerate(pmn.current_dns):
                time_left -= 1  # Simulate processing time decrement
                pmn.current_dns[i] = (dn, time_left)
                if time_left <= 0:
                    completed_dns.append(dn)

            # Remove completed DNs and update PMN mass
            for dn in completed_dns:
                if (dn, 0) in pmn.current_dns:  # Check for exact match in case of duplicates
                    pmn.current_dns = [(d, t) for d, t in pmn.current_dns if d != dn]
                pmn.mass += dn.mass
                print(f"[Complete] PMN {pmn} completed processing DN {dn}. New mass: {pmn.mass:.2f}")
                if dn in self.nodes:
                    self.nodes.remove(dn)  # Ensure the DN is removed from the simulation

            # Add new DNs if capacity allows
            while pmn.can_process_more():
                closest_dn = self.find_closest_dn(pmn)
                if closest_dn and closest_dn not in [d for d, _ in pmn.current_dns]:  # Avoid duplicates
                    processing_time = int(closest_dn.attributes.get("render_time", 10) * 10)
                    pmn.current_dns.append((closest_dn, processing_time))
                    print(f"[Start] PMN {pmn} started processing DN {closest_dn}")
                else:
                    break

        # Check for proximity and merge behavior
        self.check_proximity_and_merge()

        if self.tick_counter % 10 == 0:
            self.print_debug_info()

        self.tick_counter += 1




    def print_debug_info(self):
        print("=== Debug Info ===")
        for pmn in [node for node in self.nodes if isinstance(node, PrimaryMassNode)]:
            print(f"PMN {pmn} - Active DNs: {len(pmn.current_dns)}, Capacity: {pmn.processing_capacity:.2f}")

    def check_proximity_and_merge(self):
        proximity_threshold = self.config.get("proximity_threshold", 20)
        for node in self.nodes[:]:
            if isinstance(node, DynamicNode):
                closest_pmn = self.find_closest_pmn(node)
                if closest_pmn:
                    distance = np.linalg.norm(closest_pmn.position - node.position)
                    if distance < proximity_threshold:
                        self.merge_dn_into_pmn(node, closest_pmn)

    def merge_dn_into_pmn(self, dn, pmn):
        if len(pmn.current_dns) < pmn.threads:
            processing_time = int(dn.attributes.get("render_time", 10) * 10)
            pmn.current_dns.append((dn, processing_time))
        #    print(f"[Processing] PMN {pmn} started processing DN {dn}. Queue size: {len(pmn.current_dns)}")
        #else:
        #    print(f"[Overloaded] PMN {pmn} cannot process DN {dn}. Capacity: {len(pmn.current_dns)}/{pmn.threads}")

    def find_closest_dn(self, pmn):
        dns = [node for node in self.nodes if isinstance(node, DynamicNode)]
        if not dns:
            return None
        return min(dns, key=lambda dn: np.linalg.norm(dn.position - pmn.position))

    def find_closest_pmn(self, dynamic_node):
        pmns = [node for node in self.nodes if isinstance(node, PrimaryMassNode)]
        if not pmns:
            return None
        return min(pmns, key=lambda pmn: np.linalg.norm(pmn.position - dynamic_node.position))

    def run(self):
        app = QApplication(sys.argv)
        self.window = MainWindow(self)
        self.window.show()
        sys.exit(app.exec_())
