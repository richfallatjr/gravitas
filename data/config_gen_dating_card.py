import json

def generate_dating_config(output_file="./data/config.json"):
    config = {
        "attributes": {
            "proximity": {
                "weight": 0.8,
                "min": 0,
                "max": 100
            },
            "age_difference": {
                "weight": 0.7,
                "min": 0,
                "max": 20
            },
            "relationship_priority": {
                "weight": 0.9,
                "categories": { "high": 3, "medium": 2, "low": 1 }
            },
            "open_to_kids": {
                "weight": 0.5,
                "boolean_match": True
            }
        },
        "processing": {
            "single_process_delay": 5,
            "multi_process_threads": 4,
            "visual_timer": 15
        },
        "invert_attributes": [
            "age_difference"
        ],
        "absorption_threshold": 10,
        "mode": "multi_process"
    }

    with open(output_file, "w") as file:
        json.dump(config, file, indent=4)

    print(f"Dating config saved to {output_file}")

# Run the function to generate the config file
generate_dating_config()
