from PyQt5.QtWidgets import (
    QWidget, QMainWindow, QVBoxLayout, QPushButton, QSlider, QLabel, QHBoxLayout, QCheckBox
)
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
            if isinstance(node, DynamicNode):
                size = max(5, node.mass * 4) / 4
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
                self.draw_pmn(painter, node)

    def draw_filaments(self, painter):
        for node in self.controller.nodes:
            if isinstance(node, DynamicNode):
                closest_pmn = self.find_closest_pmn(node)
                if closest_pmn:
                    r_vector = closest_pmn.position - node.position
                    distance = np.linalg.norm(r_vector)

                    node_x = int(node.position[0])
                    node_y = int(node.position[1])
                    pmn_x = int(closest_pmn.position[0])
                    pmn_y = int(closest_pmn.position[1])

                    color = self.get_filament_gradient_color(distance)

                    pulse_opacity = int(150 + 100 * np.sin(QTime.currentTime().msecsSinceStartOfDay() / 300.0))

                    glow_pen = QPen(QColor(color.red(), color.green(), color.blue(), pulse_opacity))
                    glow_pen.setWidth(3)
                    painter.setPen(glow_pen)
                    painter.drawLine(node_x, node_y, pmn_x, pmn_y)

    def get_heatmap_gradient_color(self, distance):
        max_distance = 400
        normalized = max(0, min(1, 1 - distance / max_distance))
        
        # Define the custom purplish hue (sampled from the background and brightened)
        bright_purple = QColor(180, 100, 255)  # Adjusted to blend beautifully

        if normalized > 0.66:
            r, g, b = 77,71,88
        elif normalized > 0.33:
            r, g, b = bright_purple.red(), bright_purple.green(), bright_purple.blue()
        else:
            r, g, b = 255, 255, 255

        return QColor(r, g, b)
    
    def get_filament_gradient_color(self, distance):
        max_distance = 400
        normalized = max(0, min(1, 1 - distance / max_distance))
        
        # Define the custom purplish hue (sampled from the background and brightened)
        accent_color = QColor(118, 219, 226)  # Adjusted to blend beautifully

        if normalized > 0.66:
            #r, g, b = 255, int(255 * (1 - normalized) * 3), int(255 * (1 - normalized) * 3)
            # Mid intensity: White
            r, g, b = 255, 255, 255
        elif normalized > 0.33:
            r, g, b = accent_color.red(), accent_color.green(), accent_color.blue()
        else:
            # Low intensity: Blue to White
            r, g, b = int(255 * normalized * 3), int(255 * normalized * 3), 255

        return QColor(r, g, b)



    def find_closest_pmn(self, dynamic_node):
        pmns = [n for n in self.controller.nodes if isinstance(n, PrimaryMassNode)]
        if not pmns:
            return None
        return min(pmns, key=lambda pmn: np.linalg.norm(pmn.position - dynamic_node.position))

    def draw_pmn(self, painter, pmn):
        # Set a base size for the PMN
        base_size = 40
        max_size_increase = 20  # Limit the maximum size increase
        size = base_size + int(min(pmn.processing_capacity, 1.0) * max_size_increase)

        # Clamp the processing capacity between 0.0 and 1.0
        capacity = max(0.0, min(1.0, pmn.processing_capacity))
        color = self.get_heatmap_gradient_color(capacity * 400)  # Use 400 as a max pseudo-distance

        # Draw the glow effect
        glow_gradient = QRadialGradient(pmn.position[0], pmn.position[1], size * 2)
        glow_gradient.setColorAt(0.0, QColor(color.red(), color.green(), color.blue(), 200))
        glow_gradient.setColorAt(1.0, QColor(color.red(), color.green(), color.blue(), 0))

        painter.setBrush(glow_gradient)
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(
            int(pmn.position[0] - size),
            int(pmn.position[1] - size),
            size * 2, size * 2
        )

        # Draw the PMN itself
        painter.setBrush(QColor(color.red(), color.green(), color.blue()))
        painter.drawEllipse(
            int(pmn.position[0] - base_size / 2),
            int(pmn.position[1] - base_size / 2),
            base_size, base_size
        )



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

    def apply_dark_theme(self):
        self.setStyleSheet("""
            QMainWindow { background-color: #0A0A14; }
            QPushButton { background-color: #1E1E2F; color: #FFFFFF; border-radius: 8px; padding: 10px; }
            QPushButton:hover { background-color: #44475a; }
        """)

    def initUI(self):
        container = QWidget()
        main_layout = QVBoxLayout()

        self.simulation_view = SimulationView(self.controller)
        main_layout.addWidget(self.simulation_view, stretch=8)

        control_panel = QWidget()
        control_layout = QHBoxLayout()

        self.collision_checkbox = QCheckBox("Enable DN Collisions")
        self.collision_checkbox.setChecked(False)
        self.collision_checkbox.stateChanged.connect(self.toggle_dn_collisions)
        control_layout.addWidget(self.collision_checkbox)

        add_dn_button = QPushButton("Add Dynamic Node")
        add_dn_button.clicked.connect(self.add_dynamic_node)
        control_layout.addWidget(add_dn_button)

        add_pmn_button = QPushButton("Add Primary Mass Node")
        add_pmn_button.clicked.connect(self.add_primary_mass_node)
        control_layout.addWidget(add_pmn_button)

        self.mass_slider = QSlider(Qt.Horizontal)
        self.mass_slider.setMinimum(1)
        self.mass_slider.setMaximum(100)
        self.mass_slider.setValue(10)
        control_layout.addWidget(QLabel("Mass:"))
        control_layout.addWidget(self.mass_slider)

        start_button = QPushButton("Start Simulation")
        start_button.clicked.connect(self.start_simulation)
        control_layout.addWidget(start_button)

        control_panel.setLayout(control_layout)
        main_layout.addWidget(control_panel, stretch=1)

        container.setLayout(main_layout)
        self.setCentralWidget(container)

        self.mass_slider.valueChanged.connect(self.update_node_masses)

    def start_simulation(self):
        self.timer.start(50)
        self.simulation_view.update()

    def toggle_dn_collisions(self, state):
        self.controller.enable_dn_collisions = state == Qt.Checked

    def update_node_masses(self):
        dn_mass = self.mass_slider.value() / 10
        pmn_mass = self.mass_slider.value() * 2

        for node in self.controller.nodes:
            if isinstance(node, DynamicNode):
                node.mass = dn_mass
            elif isinstance(node, PrimaryMassNode):
                node.mass = pmn_mass
                
    def add_dynamic_node(self):
        mass = np.random.uniform(0.5, 5.0)  # Randomized mass
        position = np.random.uniform(
            [100, 100], 
            [self.simulation_view.width(), self.simulation_view.height()]
        )
        velocity_vector = (np.random.rand(2) - 0.5) * 2  # Random velocity

        new_node = DynamicNode(mass=mass, position=position, velocity=velocity_vector)
        self.controller.nodes.append(new_node)  # Add to simulation controller
        self.simulation_view.update()  # Refresh the UI
        
    def add_primary_mass_node(self):
        mass = self.mass_slider.value() * 5
        position = np.random.uniform(
            [100, 100],
            [self.simulation_view.width(), self.simulation_view.height()]
        )

        new_node = PrimaryMassNode(mass=mass, position=position, velocity=np.zeros(2))
        self.controller.nodes.append(new_node)
        self.simulation_view.update()
        
    def update_node_masses(self):
        dn_mass = self.mass_slider.value() / 10
        pmn_mass = self.mass_slider.value() * 2

        for node in self.controller.nodes:
            if isinstance(node, DynamicNode):
                node.mass = dn_mass
                speed_factor = 1 / node.mass
                node.velocity *= speed_factor
            elif isinstance(node, PrimaryMassNode):
                node.mass = pmn_mass



