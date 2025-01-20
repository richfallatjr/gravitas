import json
import numpy as np

# Configurations
CONFIG = {
    "attributes": {
        "render_time": {
            "weight": 0.7,
            "min": 1,
            "max": 15
        },
        "memory": {
            "weight": 0.5,
            "min": 1024,
            "max": 8192
        },
        "threads": {
            "weight": 0.3,
            "min": 1,
            "max": 16
        }
    },
    "invert_attributes": [
        "render_time"
    ],
    "absorption_threshold": 5,
    "processing": {
        "single_process_delay": 5,
        "multi_process_threads": 128,
        "visual_timer": 15
    },
    "mode": "multi_process"
}

# Dynamic Node (DN) generation
def generate_dn_dataset(num_dns=100):
    dn_dataset = []
    for i in range(num_dns):
        render_time = np.random.uniform(CONFIG["attributes"]["render_time"]["min"], CONFIG["attributes"]["render_time"]["max"])
        memory = np.random.uniform(CONFIG["attributes"]["memory"]["min"], CONFIG["attributes"]["memory"]["max"])
        threads = np.random.uniform(CONFIG["attributes"]["threads"]["min"], CONFIG["attributes"]["threads"]["max"])
        
        dn_dataset.append({
            "id": f"task_{i+1}",
            "attributes": {
                "render_time": render_time,
                "memory": memory,
                "threads": threads
            }
        })
    return dn_dataset

# Primary Mass Node (PMN) generation
def generate_pmn_dataset(num_pmns=5):
    pmn_dataset = []
    for i in range(num_pmns):
        threads = np.random.randint(8, 64)
        memory = np.random.uniform(8192, 65536)
        chipset_speed = f"{np.random.uniform(2.5, 4.0):.1f}GHz"
        
        preferences = {
            "render_time": np.random.uniform(0.5, 1.0),
            "threads": np.random.uniform(0.3, 0.7),
            "memory": np.random.uniform(0.1, 0.5)
        }

        pmn_dataset.append({
            "id": f"PMN_{i+1}",
            "threads": threads,
            "memory": memory,
            "chipset_speed": chipset_speed,
            "preferences": preferences
        })
    return pmn_dataset

# Save files
def save_json(filename, data):
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)
    print(f"Saved: {filename}")

# Main function
def main():
    save_json("data/config.json", CONFIG)
    save_json("data/dn_dataset.json", generate_dn_dataset())
    save_json("data/pmn_dataset.json", generate_pmn_dataset())

if __name__ == "__main__":
    main()
