import json
import math
import numpy as np

# E-commerce configuration
config = {
    "attributes": {
        "price": {"weight": 0.2, "min": 0, "max": 1000},
        "category_shoes": {"weight": 0.8, "min": 0, "max": 1},
        "category_tshirts": {"weight": 0.8, "min": 0, "max": 1},
        "category_pants": {"weight": 0.8, "min": 0, "max": 1},
        "category_hats": {"weight": 0.8, "min": 0, "max": 1},
        "category_jackets": {"weight": 0.8, "min": 0, "max": 1},
        "category_accessories": {"weight": 0.8, "min": 0, "max": 1},
        "category_bags": {"weight": 0.8, "min": 0, "max": 1}
    },
    "processing": {"single_process_delay": 5, "multi_process_threads": 128, "visual_timer": 15},
    "invert_attributes": ["price"],
    "absorption_threshold": 10,
    "mode": "multi_process"
}

# Function to normalize values
def normalize(value, min_val, max_val):
    return (value - min_val) / (max_val - min_val) if max_val != min_val else 0

# Generate DN dataset
dn_dataset = []
for i in range(300):  # Example with 500 dynamic nodes
    price = np.random.uniform(config["attributes"]["price"]["min"], config["attributes"]["price"]["max"])
    category = np.random.choice(list(config["attributes"].keys())[1:])  # Random category
    dn_attributes = {key: 0 for key in config["attributes"] if "category_" in key}  # Set all categories to 0
    dn_attributes[category] = 1  # Assign the DN to a specific category

    dn_dataset.append(
        {
            "attributes": {
                "price": normalize(price, config["attributes"]["price"]["min"], config["attributes"]["price"]["max"]),
                **dn_attributes  # Include category assignment
            }
        }
    )

# Generate PMN dataset with circular distribution
pmn_dataset = []
num_pmns = len([key for key in config["attributes"] if "category_" in key])  # One PMN per category
screen_width = 800
screen_height = 600
center_x = screen_width // 2
center_y = screen_height // 2
radius = 200  # Adjust radius for spacing from the center

for i, category in enumerate([key for key in config["attributes"] if "category_" in key]):
    angle = (2 * math.pi / num_pmns) * i
    x = center_x + radius * math.cos(angle)
    y = center_y + radius * math.sin(angle)

    pmn_dataset.append(
        {
            "preferences": {
                "price": config["attributes"]["price"]["weight"],
                category: config["attributes"][category]["weight"]
            },
            "threads": np.random.randint(4, 16),
            "position": [x, y]
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

print("Datasets generated and saved!")
