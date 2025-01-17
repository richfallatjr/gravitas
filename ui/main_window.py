# ui/main_window.py

from PyQt5.QtWidgets import QWidget, QMainWindow, QVBoxLayout, QPushButton
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtCore import QTimer
from core.node import DynamicNode, PrimaryMassNode
import numpy as np

class SimulationView(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # ✅ Draw filaments first
        self.draw_filaments(painter)

        # ✅ Draw nodes on top
        self.draw_nodes(painter)

    def draw_nodes(self, painter):
        for node in self.controller.nodes:
            if isinstance(node, DynamicNode):
                painter.setBrush(QColor(0, 100, 255))  # Blue for DNs
                size = 10
            elif isinstance(node, PrimaryMassNode):
                painter.setBrush(QColor(255, 0, 0))    # Red for PMNs
                size = 30
            painter.drawEllipse(
                int(node.position[0] - size / 2),
                int(node.position[1] - size / 2),
                size, size
            )

    def draw_filaments(self, painter):
        pen = QPen(QColor(150, 150, 150, 150))  # Gray, semi-transparent
        pen.setWidth(1)
        painter.setPen(pen)

        # ✅ Draw filaments from each DN to the nearest PMN
        for node in self.controller.nodes:
            if isinstance(node, DynamicNode):
                closest_pmn = self.find_closest_pmn(node)
                if closest_pmn:
                    painter.drawLine(
                        int(node.position[0]),
                        int(node.position[1]),
                        int(closest_pmn.position[0]),
                        int(closest_pmn.position[1])
                    )

    def find_closest_pmn(self, dynamic_node):
        pmns = [n for n in self.controller.nodes if isinstance(n, PrimaryMassNode)]
        if not pmns:
            return None

        # ✅ Find the closest PMN to the DN
        closest_pmn = min(pmns, key=lambda pmn: np.linalg.norm(pmn.position - dynamic_node.position))
        return closest_pmn

class MainWindow(QMainWindow):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setWindowTitle("SoL Gravitas - Multi-PMN Simulation")
        self.setGeometry(100, 100, 800, 600)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.controller.update)

        self.initUI()

    def initUI(self):
        container = QWidget()
        layout = QVBoxLayout()

        # ✅ Add simulation view
        self.simulation_view = SimulationView(self.controller)
        layout.addWidget(self.simulation_view)

        # ✅ Start Button
        start_button = QPushButton("Start Simulation")
        start_button.clicked.connect(self.start_simulation)
        layout.addWidget(start_button)

        container.setLayout(layout)
        self.setCentralWidget(container)

    def start_simulation(self):
        self.timer.start(50)
        self.simulation_view.update()
