import json
import numpy as np
from PIL import Image

# Configuration
config = {
    "attributes": {
        "color_red": {"weight": 1.0, "min": 0, "max": 1},
        "color_green": {"weight": 1.0, "min": 0, "max": 1},
        "color_blue": {"weight": 1.0, "min": 0, "max": 1},
    },
    "invert_attributes": [],
    "absorption_threshold": 10,
    "processing": {
        "single_process_delay": 5,
        "multi_process_threads": 128,
        "visual_timer": 15,
    },
    "mode": "multi_process",
}

def initialize_pmns():
    """
    Initializes PMNs to represent the RGB color wheel with fixed positions.
    """
    positions = [
        [200, 200],  # Red
        [400, 200],  # Green
        [600, 200],  # Blue
        [200, 400],  # Cyan
        [400, 400],  # Magenta
        [600, 400],  # Yellow
    ]
    colors = [
        {"color_red": 1.0, "color_green": 0.0, "color_blue": 0.0},  # Red
        {"color_red": 0.0, "color_green": 1.0, "color_blue": 0.0},  # Green
        {"color_red": 0.0, "color_green": 0.0, "color_blue": 1.0},  # Blue
        {"color_red": 0.0, "color_green": 1.0, "color_blue": 1.0},  # Cyan
        {"color_red": 1.0, "color_green": 0.0, "color_blue": 1.0},  # Magenta
        {"color_red": 1.0, "color_green": 1.0, "color_blue": 0.0},  # Yellow
    ]
    pmns = []
    for pos, color in zip(positions, colors):
        pmns.append(
            {
                "attributes": color,
                "position": pos,
                "threads": 8,  # Arbitrary processing threads
                "preferences": {
                    "color_red": color["color_red"],
                    "color_green": color["color_green"],
                    "color_blue": color["color_blue"],
                },
            }
        )
    return pmns

def simplify_image(image_path, target_pixels=300):
    """
    Simplifies an image to a fixed number of pixels.
    """
    image = Image.open(image_path).convert("RGB")

    # Resize the image to approximate the target pixel count
    aspect_ratio = image.width / image.height
    target_width = int((target_pixels * aspect_ratio) ** 0.5)
    target_height = int(target_pixels / target_width)
    image_resized = image.resize((target_width, target_height))

    # Flatten the image and randomly sample if necessary
    pixels = np.array(image_resized) / 255.0  # Normalize to 0-1
    pixels_flat = pixels.reshape(-1, 3)

    # Random sampling to meet the exact target pixel count
    if len(pixels_flat) > target_pixels:
        sampled_indices = np.random.choice(len(pixels_flat), target_pixels, replace=False)
        pixels_flat = pixels_flat[sampled_indices]

    return pixels_flat

def generate_dns_from_pixels(pixels):
    """
    Generates DNs from simplified pixel data.
    """
    dns = []
    for r, g, b in pixels:
        dns.append(
            {
                "attributes": {
                    "color_red": r,
                    "color_green": g,
                    "color_blue": b,
                }
            }
        )
    return dns

def save_datasets(pmns, dns, config, output_dir="./data"):
    """
    Saves the PMN, DN, and config datasets as JSON files.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)
    with open(f"{output_dir}/pmn_dataset.json", "w") as pmn_file:
        json.dump(pmns, pmn_file, indent=4)
    with open(f"{output_dir}/dn_dataset.json", "w") as dn_file:
        json.dump(dns, dn_file, indent=4)
    with open(f"{output_dir}/config.json", "w") as config_file:
        json.dump(config, config_file, indent=4)

def main():
    # Replace with your image file
    image_path = "./assets/galaxy2.png"

    # Simplify the image
    pixels = simplify_image(image_path, target_pixels=300)

    # Initialize PMNs and DNs from simplified pixels
    pmns = initialize_pmns()
    dns = generate_dns_from_pixels(pixels)

    # Save the datasets
    save_datasets(pmns, dns, config)
    print("Datasets generated and saved to the ./data directory.")

if __name__ == "__main__":
    main()
