def normalize_attribute(value, min_val, max_val, weight=1.0):
    """
    Normalize a value to a range [0, 1] and apply weight.

    Args:
        value (float): The actual value to normalize.
        min_val (float): The minimum possible value for the attribute.
        max_val (float): The maximum possible value for the attribute.
        weight (float): The weight to scale the normalized value.

    Returns:
        float: Weighted, normalized value in the range [0, weight].
    """
    if max_val == min_val:  # Avoid division by zero
        return weight
    normalized = (value - min_val) / (max_val - min_val)
    return max(0, min(normalized * weight, weight))  # Ensure within bounds
