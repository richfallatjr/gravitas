import json
import random

# Configuration for data generation
CONFIG = {
    "proximity": {"min": 1, "max": 10},
    "age_difference": {"min": 1, "max": 3},
    "relationship_priority": {"min": 1, "max": 3},  # Simplified as numeric values
    "open_to_kids": [1, 2]
}

def generate_random_dating_card():
    """
    Generate a single random dating card based on the configuration.
    """
    return {
        "attributes": {
            "proximity": random.randint(CONFIG["proximity"]["min"], CONFIG["proximity"]["max"]),
            "age_difference": random.randint(CONFIG["age_difference"]["min"], CONFIG["age_difference"]["max"]),
            "relationship_priority": random.randint(CONFIG["relationship_priority"]["min"], CONFIG["relationship_priority"]["max"]),
            "open_to_kids": random.choice(CONFIG["open_to_kids"])
        }
    }

def generate_dataset(num_profiles=100, output_file="./data/dn_dataset.json"):
    """
    Generate a dataset of random dating cards.
    
    :param num_profiles: Number of profiles to generate
    :param output_file: File to save the dataset
    """
    dataset = [generate_random_dating_card() for _ in range(num_profiles)]
    with open(output_file, "w") as file:
        json.dump(dataset, file, indent=4)
    print(f"Dataset with {num_profiles} profiles saved to {output_file}.")

if __name__ == "__main__":
    # Generate a dataset of 100 profiles
    generate_dataset(num_profiles=100)
