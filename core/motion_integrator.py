from core.node import DynamicNode, PrimaryMassNode  # ✅ Fix: Import the node classes
import numpy as np

class MotionIntegrator:
    def update_positions(self, nodes):
        for node in nodes:
            node.position += node.velocity

            # 🌀 Update trail for Dynamic Nodes
            if isinstance(node, DynamicNode):
                node.trail.append(node.position.copy())
                if len(node.trail) > 15:
                    node.trail.pop(0)

                # 💥 Remove burst particles after lifetime expires
                if hasattr(node, 'lifetime'):
                    node.lifetime -= 1
                    if node.lifetime <= 0:
                        nodes.remove(node)

            # ✅ Wall boundaries (assuming window size is 800x600)
            window_width, window_height = 800, 600
            size = 10 if node.mass == 1 else 30  # DynamicNode vs PMN

            # Left and Right Walls
            if node.position[0] - size / 2 <= 0 or node.position[0] + size / 2 >= window_width:
                node.velocity[0] *= -1  # ✅ Reverse X velocity

            # Top and Bottom Walls
            if node.position[1] - size / 2 <= 0 or node.position[1] + size / 2 >= window_height:
                node.velocity[1] *= -1  # ✅ Reverse Y velocity
