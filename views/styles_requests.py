STYLES = [
    {
        "id": 1,
        "style": "Classic",
        "price": 500
    },
    {
        "id": 2,
        "style": "Modern",
        "price": 710
    },
    {
        "id": 3,
        "style": "Vintage",
        "price": 965
    }
]


def get_all_styles():
    """Handles Server request for all STYLES"""
    return STYLES


def get_single_style(id):
    """gets a single style"""
    requested_style = None

    for style in STYLES:
        if style["id"] == id:
            requested_style = style

    return requested_style


def create_style(style):
    """Creates a new style"""
    # Get the id value of the last style in the list
    max_id = STYLES[-1]["id"]

    # Add 1 to whatever that number is
    new_id = max_id + 1

    # Add an `id` property to the style dictionary
    style["id"] = new_id

    # Add the style dictionary to the list
    STYLES.append(style)

    # Return the dictionary with `id` property added
    return style


def delete_style(id):
    """Deletes single style"""
    # Initial -1 value for style index, in case one isn't found
    style_index = -1

    # Iterate the STYLES list, but use enumerate() so that you
    # can access the index value of each item
    for index, style in enumerate(STYLES):
        if style["id"] == id:
            # Found the style. Store the current index.
            style_index = index

    # If the style was found, use pop(int) to remove it from list
    if style_index >= 0:
        STYLES.pop(style_index)


def update_style(id, new_style):
    """Updates style with Replacement"""
    # Iterate the STYLES list, but use enumerate() so that
    # you can access the index value of each item.
    for index, style in enumerate(STYLES):
        if style["id"] == id:
            # Found the style. Update the value.
            STYLES[index] = new_style
            break
