class MotionIntegrator:
    def update_positions(self, nodes):
        for node in nodes:
            #print(f"Before: {node.position}")  # ✅ Debug check
            node.position += node.velocity
            #print(f"After: {node.position}")   # ✅ Debug check