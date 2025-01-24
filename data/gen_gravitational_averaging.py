import json
import numpy as np

# Configuration for the simulation
config = {
    "attributes": {
        "gravitational_pull": {"weight": 0.8, "min": 0, "max": 1},
        "mass": {"weight": 0.7, "min": 0, "max": 1},
        "distance_from_core": {"weight": 0.9, "min": 0, "max": 1},
        "velocity": {"weight": 0.6, "min": 0, "max": 1},
        "luminosity": {"weight": 0.5, "min": 0, "max": 1}
    },
    "invert_attributes": ["distance_from_core"],
    "absorption_threshold": 20,
    "processing": {"multi_process_threads": 128, "visual_timer": 10},
    "mode": "multi_process"
}

# PMN dataset: Core and halo nodes
pmn_dataset = [
    {
        "id": "Core",
        "threads": 16,
        "preferences": {
            "gravitational_pull": 1.0,
            "mass": 1.0,
            "distance_from_core": 0.0,
            "velocity": 0.0,
            "luminosity": 0.0
        },
        "position": [400, 400]  # Center of the galaxy
    },
    {
        "id": "Halo_1",
        "threads": 8,
        "preferences": {
            "gravitational_pull": 0.7,
            "mass": 0.8,
            "distance_from_core": 0.2,
            "velocity": 0.5,
            "luminosity": 0.6
        },
        "position": [200, 400]
    },
    {
        "id": "Halo_2",
        "threads": 8,
        "preferences": {
            "gravitational_pull": 0.7,
            "mass": 0.8,
            "distance_from_core": 0.2,
            "velocity": 0.5,
            "luminosity": 0.6
        },
        "position": [600, 400]
    },
    {
        "id": "Halo_3",
        "threads": 8,
        "preferences": {
            "gravitational_pull": 0.7,
            "mass": 0.8,
            "distance_from_core": 0.2,
            "velocity": 0.5,
            "luminosity": 0.6
        },
        "position": [400, 200]
    },
    {
        "id": "Halo_4",
        "threads": 8,
        "preferences": {
            "gravitational_pull": 0.7,
            "mass": 0.8,
            "distance_from_core": 0.2,
            "velocity": 0.5,
            "luminosity": 0.6
        },
        "position": [400, 600]
    }
]

# Function to generate DN positions with a radial density gradient
def generate_dn_dataset(num_dns, core_position, radius, density_fn):
    dn_dataset = []
    for _ in range(num_dns):
        r = density_fn() * radius  # Radial distance (weighted by density function)
        theta = np.random.uniform(0, 2 * np.pi)  # Random angle
        x = core_position[0] + r * np.cos(theta)
        y = core_position[1] + r * np.sin(theta)

        # Assign random attributes
        attributes = {
            "gravitational_pull": np.random.uniform(0, 1),
            "mass": np.random.uniform(0, 1),
            "distance_from_core": r / radius,
            "velocity": np.random.uniform(0, 1),
            "luminosity": np.random.uniform(0, 1)
        }

        dn_dataset.append({"attributes": attributes, "position": [x, y]})

    return dn_dataset

# Parameters for the dataset
core_position = [400, 400]
radius = 300
num_dns = 300

# Radial density function: Higher density near the edges
density_fn = lambda: np.random.beta(2, 5)  # Skewed distribution towards the edges

# Generate DN dataset
dn_dataset = generate_dn_dataset(num_dns, core_position, radius, density_fn)

# Save datasets
with open("./data/config.json", "w") as config_file:
    json.dump(config, config_file, indent=4)

with open("./data/pmn_dataset.json", "w") as pmn_file:
    json.dump(pmn_dataset, pmn_file, indent=4)

with open("./data/dn_dataset.json", "w") as dn_file:
    json.dump(dn_dataset, dn_file, indent=4)

print("Datasets generated: config, PMNs, and DNs")
