import json

# Creating a default configuration file for the system

# Defining the default configuration
default_config = {
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
    "invert_attributes": ["render_time"],  # Lower render time is preferred
    "absorption_threshold": 5,  # Time threshold in seconds for forced absorption
    "processing": {
        "single_process_delay": 5,
        "multi_process_threads": 128,
        "visual_timer": 15
    },
    "mode": "multi_process"
}

# Saving the default configuration to a JSON file
config_output_file_path = "./data/config.json"
with open(config_output_file_path, "w") as file:
    json.dump(default_config, file, indent=4)

config_output_file_path
