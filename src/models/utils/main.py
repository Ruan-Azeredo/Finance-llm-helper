def handle_values(kwargs):
    values = {}
    for key, value in kwargs.items():
        if value is not None:
            values[key] = value
    return values