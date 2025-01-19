# Creating a default configuration file for the system

# Defining the default configuration
default_config = {
    "default_weights": {
        "threads": 0.33,
        "memory": 0.33,
        "render_time": 0.34
    },
    "invert_attributes": ["render_time"],  # Lower render time is preferred
    "absorption_threshold": 5  # Time threshold in seconds for forced absorption
}

# Saving the default configuration to a JSON file
config_output_file_path = "/mnt/data/config.json"
with open(config_output_file_path, "w") as file:
    json.dump(default_config, file, indent=4)

config_output_file_path
