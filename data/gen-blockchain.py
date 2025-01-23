import json
import numpy as np

# Blockchain-inspired GREP configuration
config = {
    "attributes": {
        "transaction_load": {"weight": 0.8, "min": 0, "max": 1},
        "node_reliability": {"weight": 0.7, "min": 0, "max": 1},
        "latency": {"weight": 0.9, "min": 0, "max": 1},
        "hash_power": {"weight": 0.6, "min": 0, "max": 1},
        "network_contribution": {"weight": 0.5, "min": 0, "max": 1},
        "propagation_efficiency": {"weight": 0.4, "min": 0, "max": 1},
    },
    "invert_attributes": ["latency"],
    "absorption_threshold": 15,
    "processing": {"multi_process_threads": 128, "visual_timer": 10},
    "mode": "multi_process",
}

# Updated PMN dataset with realistic preferences for blockchain nodes
pmn_dataset = [
    {
        "id": "Validator_1",
        "threads": 8,
        "preferences": {
            "transaction_load": 0.9,
            "node_reliability": 0.8,
            "latency": 0.2,
            "hash_power": 0.7,
            "network_contribution": 0.5,
            "propagation_efficiency": 0.6,
        },
        "position": [300, 150],  # Top-left
    },
    {
        "id": "Validator_2",
        "threads": 8,
        "preferences": {
            "transaction_load": 0.7,
            "node_reliability": 1.0,
            "latency": 0.4,
            "hash_power": 0.5,
            "network_contribution": 0.3,
            "propagation_efficiency": 0.8,
        },
        "position": [500, 150],  # Top-right
    },
    {
        "id": "Validator_3",
        "threads": 8,
        "preferences": {
            "transaction_load": 0.5,
            "node_reliability": 0.6,
            "latency": 0.8,
            "hash_power": 1.0,
            "network_contribution": 0.4,
            "propagation_efficiency": 0.3,
        },
        "position": [300, 400],  # Bottom-left
    },
    {
        "id": "Validator_4",
        "threads": 8,
        "preferences": {
            "transaction_load": 0.6,
            "node_reliability": 0.7,
            "latency": 0.9,
            "hash_power": 0.4,
            "network_contribution": 1.0,
            "propagation_efficiency": 0.5,
        },
        "position": [500, 400],  # Bottom-right
    },
    {
        "id": "Validator_5",
        "threads": 8,
        "preferences": {
            "transaction_load": 0.3,
            "node_reliability": 0.4,
            "latency": 0.7,
            "hash_power": 0.6,
            "network_contribution": 0.8,
            "propagation_efficiency": 1.0,
        },
        "position": [400, 100],  # Top-center
    },
    {
        "id": "Validator_6",
        "threads": 8,
        "preferences": {
            "transaction_load": 0.4,
            "node_reliability": 0.5,
            "latency": 0.6,
            "hash_power": 0.3,
            "network_contribution": 0.7,
            "propagation_efficiency": 0.9,
        },
        "position": [400, 450],  # Bottom-center
    },
]

# DN dataset: Generate 300 DNs with diverse attributes
dn_dataset = []
attributes = list(config["attributes"].keys())

for i in range(300):
    attributes_values = {}
    for attr in attributes:
        min_val = config["attributes"][attr]["min"]
        max_val = config["attributes"][attr]["max"]

        # Assign random values within the defined range
        raw_value = np.random.uniform(min_val, max_val)
        attributes_values[attr] = max(0.0, min(1.0, (raw_value - min_val) / (max_val - min_val)))

    dn_dataset.append({"attributes": attributes_values})

# Save datasets
with open("./data/config.json", "w") as config_file:
    json.dump(config, config_file, indent=4)

with open("./data/pmn_dataset.json", "w") as pmn_file:
    json.dump(pmn_dataset, pmn_file, indent=4)

with open("./data/dn_dataset.json", "w") as dn_file:
    json.dump(dn_dataset, dn_file, indent=4)

print("Datasets updated: config, PMNs, and DNs")
