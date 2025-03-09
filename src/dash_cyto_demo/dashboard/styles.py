"""Style definitions for the Dash Cytoscape dashboard."""

def get_base_stylesheet():
    """
    Get the base stylesheet for the Cytoscape network.

    Returns
    -------
    list
        List of style dictionaries for Cytoscape
    """
    return [
        # Style for all nodes
        {
            "selector": "node",
            "style": {
                "background-color": "#6272A3",  # Node background color
                "label": "data(label)",  # Use the 'label' field as the node text
                "width": 30,  # Node width
                "height": 30,  # Node height
                "text-valign": "center",  # Vertical alignment of label
                "text-halign": "center",  # Horizontal alignment of label
                "color": "white",  # Label text color
            },
        },
        # Style for selected nodes
        {
            "selector": "node:selected",
            "style": {
                "background-color": "#FF7700",  # Highlight color for selected nodes
                "border-width": 3,
                "border-color": "#FFD700",  # Gold border for selected nodes
                "width": 40,  # Make selected nodes slightly larger
                "height": 40,
                "text-outline-color": "#000000",  # Text outline for better visibility
                "text-outline-width": 1,
                "font-size": 14,  # Larger font for selected nodes
                "z-index": 10,  # Bring selected nodes to front
            },
        },
        # Style for all edges
        {
            "selector": "edge",
            "style": {
                "width": 2,  # Edge width
                "line-color": "#A3627C",  # Edge color
                "target-arrow-color": "#A3627C",  # Arrow color
                "target-arrow-shape": "triangle",  # Arrow shape
                "curve-style": "bezier",  # Edge curve style
                "label": "data(label)",  # Use the 'label' field for the edge text
                "text-rotation": "autorotate",  # Auto-rotate text to follow edge
                "text-margin-y": -10,  # Text margin
                "color": "#555",  # Text color
            },
        },
        # Style for edges connected to selected nodes
        {
            "selector": "node:selected ~ edge, edge[source = 'node:selected'], edge[target = 'node:selected']",
            "style": {
                "width": 3,  # Thicker edges for connections to selected nodes
                "line-color": "#FFB6C1",  # Different color for edges connected to selected nodes
                "target-arrow-color": "#FFB6C1",
                "opacity": 1,  # Full opacity for selected connections
            },
        },
    ]


def get_color_stylesheet(color_attr, color_mappings):
    """
    Get stylesheet entries for coloring nodes by attribute.

    Parameters
    ----------
    color_attr : str
        Attribute to color nodes by
    color_mappings : dict
        Dictionary mapping attribute values to colors

    Returns
    -------
    list
        List of style dictionaries for Cytoscape
    """
    if not color_attr or color_attr not in color_mappings:
        return []

    style_entries = []

    # Add a style for each category value
    for value, color in color_mappings[color_attr].items():
        style_entries.append({
            "selector": f"node[{color_attr} = '{value}']",
            "style": {
                "background-color": color
            }
        })

    return style_entries
