import os
import json
import random

# Sample products for Los Angeles Mercantile
sample_products = [
    {
        "name": "Unisex Crewneck T-Shirt",
        "category": "Men",
        "price": 25.00,
        "color": "Black",
        "size": 0.5,
        "material": "50% Polyester, 25% Cotton, 25% Rayon",
        "availability": "In Stock",
        "rating": 4.5
    },
    {
        "name": "Women’s Flowy Tank",
        "category": "Women",
        "price": 30.00,
        "color": "White",
        "size": 0.25,
        "material": "100% Cotton",
        "availability": "In Stock",
        "rating": 4.7
    },
    {
        "name": "Ceramic Planter",
        "category": "Home",
        "price": 20.00,
        "color": "Beige",
        "size": 0.5,
        "material": "Ceramic",
        "availability": "In Stock",
        "rating": 4.8
    },
    {
        "name": "Men’s Hoodie",
        "category": "Men",
        "price": 50.00,
        "color": "Gray",
        "size": 0.75,
        "material": "80% Cotton, 20% Polyester",
        "availability": "In Stock",
        "rating": 4.6
    },
    {
        "name": "Women’s Tote Bag",
        "category": "Women",
        "price": 15.00,
        "color": "Blue",
        "size": 0.5,
        "material": "Canvas",
        "availability": "In Stock",
        "rating": 4.9
    },
    {
        "name": "Decorative Pillow",
        "category": "Home",
        "price": 40.00,
        "color": "Green",
        "size": 0.5,
        "material": "Linen",
        "availability": "In Stock",
        "rating": 4.7
    }
]

# Generate DN dataset with 300 entries
dn_dataset = []
for _ in range(450):
    product = random.choice(sample_products)
    attributes = {
        "price": product["price"] / 100,  # Normalize price assuming max $100
        "category": product["category"],
        "rating": product["rating"] / 5,  # Normalize rating assuming max 5
        "availability": 1.0 if product["availability"] == "In Stock" else 0.0,
        "size": product["size"],  # Represent size as length of string (proxy value)
        "color": hash(product["color"]) % 100 / 100.0,  # Hash color to a 0-1 value
    }
    dn_dataset.append({"attributes": attributes, "product_name": product["name"]})

# PMN dataset for categories
pmn_dataset = [
    {
        "id": "Men",
        "threads": 8,
        "preferences": {
            "price": 0.7,
            "rating": 0.8,
            "availability": 0.6,
            "size": 0.4,
            "color": 0.5
        },
        "position": [200, 200]
    },
    {
        "id": "Women",
        "threads": 8,
        "preferences": {
            "price": 0.8,
            "rating": 0.9,
            "availability": 0.7,
            "size": 0.5,
            "color": 0.6
        },
        "position": [600, 200]
    },
    {
        "id": "Home",
        "threads": 8,
        "preferences": {
            "price": 0.6,
            "rating": 0.7,
            "availability": 0.8,
            "size": 0.9,
            "color": 0.7
        },
        "position": [400, 400]
    }
]

# Config for this setup
config = {
    "attributes": {
        "price": {"weight": 0.7, "min": 0, "max": 1},
        "rating": {"weight": 0.8, "min": 0, "max": 1},
        "availability": {"weight": 0.6, "min": 0, "max": 1},
        "size": {"weight": 0.5, "min": 0, "max": 1},
        "color": {"weight": 0.4, "min": 0, "max": 1}
    },
    "invert_attributes": [],
    "absorption_threshold": 15,
    "processing": {"multi_process_threads": 128, "visual_timer": 10},
    "mode": "multi_process"
}

# Ensure output directory exists
output_dir = "./data/"
os.makedirs(output_dir, exist_ok=True)

# Save datasets to JSON files
datasets = {
    "config.json": config,
    "pmn_dataset.json": pmn_dataset,
    "dn_dataset.json": dn_dataset
}

for filename, data in datasets.items():
    with open(output_dir + filename, "w") as file:
        json.dump(data, file, indent=4)

print("Datasets for Los Angeles Mercantile-inspired GREP setup have been successfully generated!")
