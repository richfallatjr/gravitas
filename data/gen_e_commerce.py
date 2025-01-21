import json
import numpy as np

# Configuration
config = {
    "attributes": {
        "price": {"weight": 0.7, "min": 0, "max": 500},
        "rating": {"weight": 0.5, "min": 1, "max": 5},
        "popularity": {"weight": 0.6, "min": 1, "max": 1000},
        "discount": {"weight": 0.4, "min": 0, "max": 50}
    },
    "invert_attributes": ["price"],
}

# Normalize helper
def normalize(value, min_val, max_val):
    return (value - min_val) / (max_val - min_val) if max_val != min_val else 0

# Generate DNs (products)
dn_dataset = []
for i in range(300):  # Example with 1000 products
    price = np.random.uniform(config["attributes"]["price"]["min"], config["attributes"]["price"]["max"])
    rating = np.random.uniform(config["attributes"]["rating"]["min"], config["attributes"]["rating"]["max"])
    popularity = np.random.randint(config["attributes"]["popularity"]["min"], config["attributes"]["popularity"]["max"])
    discount = np.random.uniform(config["attributes"]["discount"]["min"], config["attributes"]["discount"]["max"])

    dn_dataset.append({
        "attributes": {
            "price": normalize(price, config["attributes"]["price"]["min"], config["attributes"]["price"]["max"]),
            "rating": normalize(rating, config["attributes"]["rating"]["min"], config["attributes"]["rating"]["max"]),
            "popularity": normalize(popularity, config["attributes"]["popularity"]["min"], config["attributes"]["popularity"]["max"]),
            "discount": normalize(discount, config["attributes"]["discount"]["min"], config["attributes"]["discount"]["max"]),
        }
    })

# Generate PMNs (users)
pmn_dataset = []
for i in range(5):  # Example with 5 user clusters
    preferences = {
        "price": np.random.uniform(0.5, 1.0),
        "rating": np.random.uniform(0.5, 1.0),
        "popularity": np.random.uniform(0.5, 1.0),
        "discount": np.random.uniform(0.5, 1.0),
    }
    pmn_dataset.append({
        "preferences": preferences,
        "threads": np.random.randint(4, 16),
        "position": np.random.uniform([100, 100], [700, 500]).tolist(),
    })

# Save datasets
with open("./data/dn_dataset.json", "w") as dn_file:
    json.dump(dn_dataset, dn_file, indent=4)

with open("./data/pmn_dataset.json", "w") as pmn_file:
    json.dump(pmn_dataset, pmn_file, indent=4)

config_file_path = "./data/config.json"
with open(config_file_path, "w") as config_file:
    json.dump(config, config_file, indent=4)