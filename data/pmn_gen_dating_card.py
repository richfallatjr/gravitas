import json
import numpy as np

# Configuration for PMN attributes
pmn_config = {
    "threads": {
        "min": 4,
        "max": 16
    },
    "proximity": {
        "min": 0,
        "max": 100
    },
    "relationship_priority": {
        "min": 1,
        "max": 3
    },
    "open_to_kids": {
        "min": 0,
        "max": 1
    }
}

def generate_random_pmn_data(num_pmns=10):
    """
    Generate random PMN data for the dating card application.
    Each PMN will have attributes consistent with the dataset schema.
    """
    pmn_data = []
    for _ in range(num_pmns):
        pmn = {
            "threads": int(np.random.uniform(pmn_config["threads"]["min"], pmn_config["threads"]["max"])),
            "proximity": float(np.random.uniform(pmn_config["proximity"]["min"], pmn_config["proximity"]["max"])),
            "relationship_priority": int(np.random.uniform(pmn_config["relationship_priority"]["min"], pmn_config["relationship_priority"]["max"])),
            "open_to_kids": int(np.random.uniform(pmn_config["open_to_kids"]["min"], pmn_config["open_to_kids"]["max"]))
        }
        pmn_data.append(pmn)
    return pmn_data

def save_pmn_data(file_path, pmn_data):
    """
    Save PMN data to a JSON file.
    """
    with open(file_path, "w") as file:
        json.dump(pmn_data, file, indent=4)

if __name__ == "__main__":
    # Generate PMN data
    num_pmns = 20  # Set the number of PMNs you want to generate
    pmn_data = generate_random_pmn_data(num_pmns)

    # Save to file
    file_path = "./data/pmn_dataset.json"
    save_pmn_data(file_path, pmn_data)
    print(f"PMN dataset saved to {file_path}")
