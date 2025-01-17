# core/simulation_controller.py

from ui.main_window import MainWindow
from core.force_calculator import ForceCalculator
from core.motion_integrator import MotionIntegrator
from core.collision_handler import CollisionHandler
from core.node import DynamicNode, PrimaryMassNode
from PyQt5.QtWidgets import QApplication
import sys

class SimulationController:
    def __init__(self):
        self.force_calculator = ForceCalculator()
        self.motion_integrator = MotionIntegrator()
        self.collision_handler = CollisionHandler()
        self.nodes = []
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
        self.force_calculator.apply_forces(self.nodes)
        self.motion_integrator.update_positions(self.nodes)

        # Refresh the UI
        if self.window and hasattr(self.window, 'simulation_view'):
            self.window.simulation_view.update()

    def run(self):
        app = QApplication(sys.argv)
        self.window = MainWindow(self)
        self.window.show()
        sys.exit(app.exec_())
