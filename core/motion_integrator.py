from core.node import DynamicNode, PrimaryMassNode
import numpy as np

class MotionIntegrator:
    def __init__(self, window_width=800, window_height=600):
        """
        Initialize the motion integrator with optional window dimensions.

        :param window_width: Width of the simulation area.
        :param window_height: Height of the simulation area.
        """
        self.window_width = window_width
        self.window_height = window_height

    def update_positions(self, nodes):
        """
        Update the positions of all nodes based on their velocities and manage boundaries.
        """
        for node in nodes:
            # Update position based on velocity
            node.position += node.velocity

            # Update trail for Dynamic Nodes
            if isinstance(node, DynamicNode):
                self.update_trail(node)
                self.handle_lifetime(node, nodes)

            # Handle wall boundaries
            self.handle_boundaries(node)

    def update_trail(self, node):
        """
        Update the trail of a DynamicNode, maintaining a fixed length.

        :param node: The DynamicNode to update.
        """
        node.trail.append(node.position.copy())
        max_trail_length = 15  # Configurable trail length
        if len(node.trail) > max_trail_length:
            node.trail.pop(0)

    def handle_lifetime(self, node, nodes):
        """
        Remove nodes if their lifetime expires (optional for burst effects).

        :param node: The node to check for lifetime expiration.
        :param nodes: The list of all nodes in the simulation.
        """
        if hasattr(node, 'lifetime'):
            node.lifetime -= 1
            if node.lifetime <= 0:
                nodes.remove(node)

    def handle_boundaries(self, node):
        """
        Reflect nodes off the walls of the simulation area.

        :param node: The node to check for boundary collisions.
        """
        size = self.get_node_size(node)

        # Left and Right Walls
        if node.position[0] - size / 2 <= 0 or node.position[0] + size / 2 >= self.window_width:
            node.velocity[0] *= -1  # Reverse X velocity

        # Top and Bottom Walls
        if node.position[1] - size / 2 <= 0 or node.position[1] + size / 2 >= self.window_height:
            node.velocity[1] *= -1  # Reverse Y velocity

    def get_node_size(self, node):
        """
        Determine the size of a node based on its attributes or type.

        :param node: The node to determine size for.
        :return: The size of the node.
        """
        if isinstance(node, DynamicNode):
            return 10  # Example size for DynamicNode
        elif isinstance(node, PrimaryMassNode):
            return 30  # Example size for PrimaryMassNode
        return 20  # Default size for unknown nodes
