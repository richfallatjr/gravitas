# Rewriting the code after environment reset to create the DN JSON dataset

import json

# Defining the categories for DNs
categories = {
    "categories": [
        {
            "category_id": "category_1",
            "frames": 10,
            "attributes": {
                "threads": 8,
                "memory": 2048,
                "render_time": 5
            }
        },
        {
            "category_id": "category_2",
            "frames": 10,
            "attributes": {
                "threads": 12,
                "memory": 4096,
                "render_time": 10
            }
        },
        {
            "category_id": "category_3",
            "frames": 10,
            "attributes": {
                "threads": 16,
                "memory": 8192,
                "render_time": 15
            }
        }
    ]
}

# Generating individual DNs based on categories
dn_dataset = []
for category in categories["categories"]:
    for i in range(1, category["frames"] + 1):
        dn = {
            "id": f"{category['category_id']}_frame_{i}",
            "attributes": category["attributes"]
        }
        dn_dataset.append(dn)

# Saving the dataset to a JSON file
output_file_path = "/mnt/data/dn_dataset.json"
with open(output_file_path, "w") as file:
    json.dump(dn_dataset, file, indent=4)

output_file_path
