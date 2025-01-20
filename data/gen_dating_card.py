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

# Generate DN dataset
dn_dataset = []
for i in range(100):  # Example with 100 dynamic nodes
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

# Generate PMN dataset
pmn_dataset = []
for i in range(5):  # Example with 5 primary mass nodes
    proximity_pref = np.random.uniform(0.5, 1.0)  # Weight preferences
    age_diff_pref = np.random.uniform(0.5, 1.0)
    relationship_priority_pref = np.random.uniform(0.5, 1.0)
    open_to_kids_pref = np.random.uniform(0.5, 1.0)

    pmn_dataset.append(
        {
            "preferences": {
                "proximity": proximity_pref,
                "age_difference": age_diff_pref,
                "relationship_priority": relationship_priority_pref,
                "open_to_kids": open_to_kids_pref,
            },
            "threads": np.random.randint(4, 16),
            "position": np.random.uniform([100, 100], [700, 500]).tolist(),  # Random position
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

(dn_file_path, pmn_file_path, config_file_path)
