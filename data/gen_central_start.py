import json
import numpy as np

# Kubernetes-inspired GREP configuration
config = {
    "attributes": {
        "cpu_request": {"weight": 0.8, "min": 0, "max": 1},
        "memory_request": {"weight": 0.7, "min": 0, "max": 1},
        "priority": {"weight": 0.9, "min": 0, "max": 1},
        "network_bandwidth": {"weight": 0.6, "min": 0, "max": 1},
        "scaling_factor": {"weight": 0.5, "min": 0, "max": 1},
        "latency_sensitivity": {"weight": 0.7, "min": 0, "max": 1},
    },
    "invert_attributes": ["latency_sensitivity"],
    "absorption_threshold": 15,
    "processing": {"multi_process_threads": 128, "visual_timer": 10},
    "mode": "multi_process",
}

# PMN dataset: Representing Kubernetes nodes
pmn_dataset = []
attributes = list(config["attributes"].keys())
positions = [
    [200, 200],  # Top-left
    [600, 200],  # Top-right
    [200, 500],  # Bottom-left
    [600, 500],  # Bottom-right
    [400, 100],  # Top-center
    [400, 400],  # Center
]

# Limit PMNs to 6 and distribute them evenly on screen
for i in range(6):  # 6 PMNs
    preferences = {attr: 0.0 for attr in attributes}  # Default no weight
    preferences[attributes[i % len(attributes)]] = 1.0  # Strong preference for specific attribute

    pmn_dataset.append({
        "id": f"Node_{i+1}",
        "threads": np.random.randint(4, 9),  # Random thread count between 4 and 8
        "preferences": preferences,
        "position": positions[i]  # Evenly distributed positions
    })

# DN dataset: Representing Kubernetes pods/workloads
dn_dataset = []
center_position = [400, 300]  # Center position for all DNs
for i in range(300):  # 300 DNs
    attributes_values = {}
    for attr in attributes:
        min_val = config["attributes"][attr]["min"]
        max_val = config["attributes"][attr]["max"]

        # Assign random values within the defined range
        raw_value = np.random.uniform(min_val, max_val)
        attributes_values[attr] = max(0.0, min(1.0, (raw_value - min_val) / (max_val - min_val)))

    dn_dataset.append({
        "attributes": attributes_values,
        "position": center_position  # Start all DNs at the center
    })

# Save datasets
output_dir = "./data/"
datasets = {
    "config.json": config,
    "pmn_dataset.json": pmn_dataset,
    "dn_dataset.json": dn_dataset
}

for filename, data in datasets.items():
    with open(output_dir + filename, "w") as file:
        json.dump(data, file, indent=4)

print("Datasets for Kubernetes-inspired GREP setup have been successfully generated!")
