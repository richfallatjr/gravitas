# Creating a JSON dataset for PMNs with at least 3 examples and different characteristics

# Defining the PMN dataset
pmn_dataset = [
    {
        "id": "PMN1",
        "threads": 16,
        "memory": 8192,
        "chipset_speed": "3.2GHz",
        "preferences": {
            "render_time": 0.6,
            "threads": 0.3,
            "memory": 0.1
        }
    },
    {
        "id": "PMN2",
        "threads": 32,
        "memory": 16384,
        "chipset_speed": "3.8GHz",
        "preferences": {
            "render_time": 0.4,
            "threads": 0.4,
            "memory": 0.2
        }
    },
    {
        "id": "PMN3",
        "threads": 8,
        "memory": 4096,
        "chipset_speed": "2.5GHz",
        "preferences": {
            "render_time": 0.5,
            "threads": 0.2,
            "memory": 0.3
        }
    }
]

# Saving the PMN dataset to a JSON file
pmn_output_file_path = "/mnt/data/pmn_dataset.json"
with open(pmn_output_file_path, "w") as file:
    json.dump(pmn_dataset, file, indent=4)

pmn_output_file_path