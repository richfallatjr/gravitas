import sys
import random
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtCore import Qt, QTimer

class Node:
    def __init__(self, x, y, radius=5):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = QColor(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

class SimulationWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.nodes = [Node(random.randint(50, 450), random.randint(50, 450)) for _ in range(20)]
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_simulation)
        self.timer.start(50)  # Update every 50ms

    def update_simulation(self):
        # Randomly move nodes slightly to simulate jitter
        for node in self.nodes:
            node.x += random.randint(-2, 2)
            node.y += random.randint(-2, 2)
        self.update()  # Trigger repaint

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        for node in self.nodes:
            painter.setBrush(node.color)
            painter.drawEllipse(node.x, node.y, node.radius * 2, node.radius * 2)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt5 Node Simulation")
        self.setGeometry(100, 100, 500, 500)

        self.simulation_widget = SimulationWidget()
        self.setCentralWidget(self.simulation_widget)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
