# ui/main_window.py

from PyQt5.QtWidgets import QWidget, QMainWindow, QVBoxLayout, QPushButton, QSlider, QLabel, QHBoxLayout, QCheckBox
from PyQt5.QtGui import QPainter, QColor, QPen, QRadialGradient, QPixmap
from PyQt5.QtCore import QTimer, Qt, QTime
from core.node import DynamicNode, PrimaryMassNode
import numpy as np
import math


class SimulationView(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.background = QPixmap("assets/icons/nebula_background_resized.png")

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        self.draw_background(painter)
        self.draw_filaments(painter)
        self.draw_nodes(painter)

    def draw_background(self, painter):
        painter.drawPixmap(self.rect(), self.background)

    def draw_nodes(self, painter):
        pulse_factor = (math.sin(QTime.currentTime().msecsSinceStartOfDay() / 500.0) + 1) / 2

        for node in self.controller.nodes:
            # ✅ Skip nodes with invalid (NaN) positions
            if np.isnan(node.position).any():
                continue

            if isinstance(node, DynamicNode):
                size = max(5, node.mass * 4)
                
                glow_gradient = QRadialGradient(node.position[0], node.position[1], size * 4)
                glow_gradient.setColorAt(0.0, QColor(0, 150, 255, int((150 + pulse_factor * 50) * 0.33)))
                glow_gradient.setColorAt(1.0, QColor(0, 150, 255, 0))

                painter.setBrush(glow_gradient)
                painter.setPen(Qt.NoPen)
                painter.drawEllipse(
                    int(node.position[0] - size * 2),
                    int(node.position[1] - size * 2),
                    size * 4, size * 4
                )

                painter.setBrush(QColor(0, 150, 255))
                painter.drawEllipse(int(node.position[0] - size / 2), int(node.position[1] - size / 2), size, size)

            elif isinstance(node, PrimaryMassNode):
                size = 40
                glow_gradient = QRadialGradient(node.position[0], node.position[1], size * 6)
                glow_gradient.setColorAt(0.0, QColor(255, 255, 150, int((180 + pulse_factor * 75) * 0.33)))
                glow_gradient.setColorAt(1.0, QColor(255, 255, 150, 0))

                painter.setBrush(glow_gradient)
                painter.setPen(Qt.NoPen)
                painter.drawEllipse(
                    int(node.position[0] - size * 3),
                    int(node.position[1] - size * 3),
                    size * 6, size * 6
                )

                painter.setBrush(QColor(255, 255, 150))
                painter.drawEllipse(int(node.position[0] - size / 2), int(node.position[1] - size / 2), size, size)

    def draw_filaments(self, painter):
        for node in self.controller.nodes:
            if isinstance(node, DynamicNode):
                closest_pmn = self.find_closest_pmn(node)
                if closest_pmn:
                    r_vector = closest_pmn.position - node.position
                    distance = np.linalg.norm(r_vector)

                    # ✅ Clamp positions to prevent overflow
                    node_x = np.clip(int(node.position[0]), -2000, 2000)
                    node_y = np.clip(int(node.position[1]), -2000, 2000)
                    pmn_x = np.clip(int(closest_pmn.position[0]), -2000, 2000)
                    pmn_y = np.clip(int(closest_pmn.position[1]), -2000, 2000)

                    # 🔥 Heatmap gradient based on distance
                    color = self.get_heatmap_gradient_color(distance)

                    pulse_opacity = int(150 + 100 * np.sin(QTime.currentTime().msecsSinceStartOfDay() / 300.0))

                    glow_pen = QPen(QColor(color.red(), color.green(), color.blue(), pulse_opacity))
                    glow_pen.setWidth(3)
                    painter.setPen(glow_pen)
                    painter.drawLine(node_x, node_y, pmn_x, pmn_y)

    def get_heatmap_gradient_color(self, distance):
        max_distance = 400
        normalized = max(0, min(1, 1 - distance / max_distance))

        if normalized > 0.66:
            r, g, b = 255, int(255 * (1 - normalized) * 3), int(255 * (1 - normalized) * 3)
        elif normalized > 0.33:
            r, g, b = 255, 0, int(255 * (normalized - 0.33) * 3)
        else:
            r, g, b = int(255 * normalized * 3), 0, 255

        return QColor(r, g, b)

    def find_closest_pmn(self, dynamic_node):
        pmns = [n for n in self.controller.nodes if isinstance(n, PrimaryMassNode)]
        if not pmns:
            return None
        return min(pmns, key=lambda pmn: np.linalg.norm(pmn.position - dynamic_node.position))


class MainWindow(QMainWindow):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setWindowTitle("SoL Gravitas - Multi-PMN Simulation")
        self.setGeometry(100, 100, 800, 600)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.controller.update)

        self.apply_dark_theme()
        self.initUI()
        
    def update_node_masses(self):
        # 🎯 Scale slider value for DNs and PMNs differently
        dn_mass = self.mass_slider.value() / 10
        pmn_mass = self.mass_slider.value() * 2

        for node in self.controller.nodes:
            if isinstance(node, DynamicNode):
                node.mass = dn_mass

                # ✅ Adjust velocity inversely with mass
                speed_factor = 1 / node.mass  # Heavier → slower, lighter → faster
                node.velocity *= speed_factor

            elif isinstance(node, PrimaryMassNode):
                node.mass = pmn_mass
                # 🔒 PMNs usually don't move, so no velocity adjustment needed

    def add_dynamic_node(self):
        mass = np.random.uniform(0.5, 5.0)
        position = np.random.rand(2) * [self.simulation_view.width(), self.simulation_view.height()]
        velocity_vector = (np.random.rand(2) - 0.5) * 2

        new_node = DynamicNode(mass=mass, position=position, velocity=velocity_vector)
        self.controller.nodes.append(new_node)
        self.simulation_view.update()

    def add_primary_mass_node(self):
        mass = self.mass_slider.value() * 5
        position = np.random.rand(2) * [self.simulation_view.width(), self.simulation_view.height()]

        new_node = PrimaryMassNode(mass=mass, position=position, velocity=np.zeros(2))
        self.controller.nodes.append(new_node)
        self.simulation_view.update()

    def apply_dark_theme(self):
        self.setStyleSheet("""
            QMainWindow { background-color: #0A0A14; }
            QPushButton { background-color: #1E1E2F; color: #FFFFFF; border-radius: 8px; padding: 10px; }
            QPushButton:hover { background-color: #44475a; }
        """)

    def initUI(self):
        container = QWidget()
        main_layout = QVBoxLayout()  # Vertical layout for simulation and controls

        # ✅ Simulation View (Expands)
        self.simulation_view = SimulationView(self.controller)
        main_layout.addWidget(self.simulation_view, stretch=8)  # Give more space to simulation

        # ✅ Control Panel Layout (Fixed height)
        control_panel = QWidget()
        control_layout = QHBoxLayout()
        
        # ➕ Add Collision Toggle Checkbox
        self.collision_checkbox = QCheckBox("Enable DN Collisions")
        self.collision_checkbox.setChecked(False)  # Default: Collisions OFF
        self.collision_checkbox.stateChanged.connect(self.toggle_dn_collisions)
        control_layout.addWidget(self.collision_checkbox)

        # ➕ Add Dynamic Node Button
        add_dn_button = QPushButton("Add Dynamic Node")
        add_dn_button.clicked.connect(self.add_dynamic_node)
        control_layout.addWidget(add_dn_button)

        # ➕ Add Primary Mass Node Button
        add_pmn_button = QPushButton("Add Primary Mass Node")
        add_pmn_button.clicked.connect(self.add_primary_mass_node)
        control_layout.addWidget(add_pmn_button)

        # ⚙️ Mass Slider
        self.mass_slider = QSlider(Qt.Horizontal)
        self.mass_slider.setMinimum(1)
        self.mass_slider.setMaximum(100)
        self.mass_slider.setValue(10)
        control_layout.addWidget(QLabel("Mass:"))
        control_layout.addWidget(self.mass_slider)

        # ▶️ Start Button
        start_button = QPushButton("Start Simulation")
        start_button.clicked.connect(self.start_simulation)
        control_layout.addWidget(start_button)

        # ✅ Apply layout to the control panel
        control_panel.setLayout(control_layout)
        main_layout.addWidget(control_panel, stretch=1)  # Less space for controls

        # ✅ Set the main layout
        container.setLayout(main_layout)
        self.setCentralWidget(container)
        
        # 🎛️ Connect slider changes to mass update
        self.mass_slider.valueChanged.connect(self.update_node_masses)

    def start_simulation(self):
        self.timer.start(50)
        self.simulation_view.update()
        
    def toggle_dn_collisions(self, state):
        self.controller.enable_dn_collisions = state == Qt.Checked
