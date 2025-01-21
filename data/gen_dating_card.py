import json
import numpy as np

# Dating card configuration
config = {
    "attributes": {
        "proximity": {"weight": 0.8, "min": 0, "max": 10},
        "age_difference": {"weight": 0.7, "min": 0, "max": 20},
        "relationship_priority": {"weight": 0.9, "min": 1, "max": 3},
        "open_to_kids": {"weight": 0.5, "min": 0, "max": 1},
    },
    "processing": {"single_process_delay": 5, "multi_process_threads": 128, "visual_timer": 15},
    "invert_attributes": ["age_difference", "proximity"],
    "absorption_threshold": 10,
    "mode": "multi_process",
}

# Function to normalize values
def normalize(value, min_val, max_val):
    return (value - min_val) / (max_val - min_val) if max_val != min_val else 0

# Generate DN dataset (100,000 nodes)
dn_dataset = []
for i in range(300):  # Scaling up to 100,000 nodes
    proximity = np.random.uniform(config["attributes"]["proximity"]["min"], config["attributes"]["proximity"]["max"])
    age_difference = np.random.uniform(
        config["attributes"]["age_difference"]["min"], config["attributes"]["age_difference"]["max"]
    )
    relationship_priority = np.random.randint(
        config["attributes"]["relationship_priority"]["min"], config["attributes"]["relationship_priority"]["max"] + 1
    )
    open_to_kids = np.random.choice([0, 1])  # Boolean as 0 or 1

    dn_dataset.append(
        {
            "attributes": {
                "proximity": normalize(proximity, config["attributes"]["proximity"]["min"], config["attributes"]["proximity"]["max"]),
                "age_difference": normalize(age_difference, config["attributes"]["age_difference"]["min"], config["attributes"]["age_difference"]["max"]),
                "relationship_priority": normalize(relationship_priority, config["attributes"]["relationship_priority"]["min"], config["attributes"]["relationship_priority"]["max"]),
                "open_to_kids": normalize(open_to_kids, config["attributes"]["open_to_kids"]["min"], config["attributes"]["open_to_kids"]["max"]),
            }
        }
    )

# Generate PMN dataset with balanced grid layout
pmn_dataset = []
grid_size = 5  # Example: 5x5 grid
grid_spacing = 200  # Spacing between PMNs
start_x, start_y = 100, 100  # Starting position for the grid

for i in range(grid_size):
    for j in range(grid_size):
        x = start_x + i * grid_spacing
        y = start_y + j * grid_spacing
        preferences = {
            "proximity": np.random.uniform(0.5, 1.0),
            "age_difference": np.random.uniform(0.5, 1.0),
            "relationship_priority": np.random.uniform(0.5, 1.0),
            "open_to_kids": np.random.uniform(0.5, 1.0),
        }
        pmn_dataset.append({
            "preferences": preferences,
            "threads": np.random.randint(4, 16),
            "position": [x, y],
        })

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

print(f"Generated datasets:\n- DNs: {dn_file_path}\n- PMNs: {pmn_file_path}\n- Config: {config_file_path}")
