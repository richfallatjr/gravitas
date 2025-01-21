import json
import numpy as np

# PropertyShare configuration
config = {
    "attributes": {
        "proximity": {"weight": 0.8, "min": 0, "max": 100},
        "property_value": {"weight": 0.7, "min": 100000, "max": 1000000},
        "occupancy_rate": {"weight": 0.6, "min": 0, "max": 1},
        "shared_credit_willingness": {"weight": 0.5, "min": 0, "max": 1},
    },
    "processing": {"single_process_delay": 5, "multi_process_threads": 128, "visual_timer": 15},
    "invert_attributes": ["proximity"],  # Inverted for closer is better
    "absorption_threshold": 10,
    "mode": "multi_process",
}

# Generate Dynamic Node (DN) dataset
dn_dataset = []
for i in range(300):  # Simulating 1000 properties
    proximity = np.random.uniform(config["attributes"]["proximity"]["min"], config["attributes"]["proximity"]["max"])
    property_value = np.random.uniform(
        config["attributes"]["property_value"]["min"], config["attributes"]["property_value"]["max"]
    )
    occupancy_rate = np.random.uniform(config["attributes"]["occupancy_rate"]["min"], config["attributes"]["occupancy_rate"]["max"])
    shared_credit_willingness = np.random.uniform(
        config["attributes"]["shared_credit_willingness"]["min"], config["attributes"]["shared_credit_willingness"]["max"]
    )

    dn_dataset.append(
        {
            "attributes": {
                "proximity": proximity,
                "property_value": property_value,
                "occupancy_rate": occupancy_rate,
                "shared_credit_willingness": shared_credit_willingness,
            },
            "position": np.random.uniform([100, 100], [700, 500]).tolist(),  # Random position for visualization
        }
    )

# Generate Primary Mass Node (PMN) dataset
pmn_dataset = []

# Define positions for 3 evenly distributed PMNs
canvas_width, canvas_height = 800, 600
positions = [
    [canvas_width * 0.25, canvas_height * 0.5],  # Left
    [canvas_width * 0.5, canvas_height * 0.5],   # Center
    [canvas_width * 0.75, canvas_height * 0.5],  # Right
]

for i, position in enumerate(positions):
    proximity_pref = np.random.uniform(0.5, 1.0)  # Weight preferences
    property_value_pref = np.random.uniform(0.5, 1.0)
    occupancy_rate_pref = np.random.uniform(0.5, 1.0)
    shared_credit_pref = np.random.uniform(0.5, 1.0)

    pmn_dataset.append(
        {
            "preferences": {
                "proximity": proximity_pref,
                "property_value": property_value_pref,
                "occupancy_rate": occupancy_rate_pref,
                "shared_credit_willingness": shared_credit_pref,
            },
            "threads": np.random.randint(4, 16),
            "position": position,
        }
    )

# Save datasets
dn_file_path = "./data/dn_dataset.json"
pmn_file_path = "./data/pmn_dataset.json"
config_file_path = "./data/config.json"

with open(dn_file_path, "w") as dn_file:
    json.dump(dn_dataset, dn_file, indent=4)

with open(pmn_file_path, "w") as pmn_file:
    json.dump(pmn_dataset, pmn_file, indent=4)

with open(config_file_path, "w") as config_file:
    json.dump(config, config_file, indent=4)

print("PropertyShare dataset with 3 PMNs generated successfully!")
