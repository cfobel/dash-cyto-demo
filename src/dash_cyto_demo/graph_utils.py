"""Utility functions for working with graphs."""

import functools
import colorsys
import logging

import networkx as nx
from networkx.readwrite import json_graph

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Create partial functions with explicit edges parameter to avoid deprecation warnings
node_link_data_with_links = functools.partial(json_graph.node_link_data, edges="links")
node_link_graph_with_links = functools.partial(json_graph.node_link_graph, edges="links")

def get_graph_info(G):
    """
    Get information about a graph as a string.

    Parameters
    ----------
    G : networkx.Graph
        The graph to get information about

    Returns
    -------
    str
        String containing graph information
    """
    return (
        f"Type: {type(G).__name__}, "
        f"Nodes: {G.number_of_nodes()}, "
        f"Edges: {G.number_of_edges()}"
    )


def generate_color_palette(n_colors):
    """
    Generate a palette of distinct colors.

    Parameters
    ----------
    n_colors : int
        Number of colors to generate

    Returns
    -------
    list
        List of hex color codes
    """
    palette = []
    for i in range(n_colors):
        # Use HSV color space for evenly distributed distinct colors
        hue = i / n_colors
        # Keep saturation and value high for vibrant colors
        saturation = 0.7
        value = 0.9

        # Convert to RGB
        r, g, b = colorsys.hsv_to_rgb(hue, saturation, value)

        # Convert to hex
        hex_color = "#{:02x}{:02x}{:02x}".format(
            int(r * 255), int(g * 255), int(b * 255)
        )
        palette.append(hex_color)

    return palette


def extract_categorical_attributes(graph_data):
    """
    Extract categorical attributes from graph data.

    Parameters
    ----------
    graph_data : dict
        Graph data in Cytoscape format

    Returns
    -------
    dict
        Dictionary of categorical attributes and their unique values
    """
    node_attributes = set()
    categorical_attributes = {}

    for node in graph_data["elements"]["nodes"]:
        for attr, value in node["data"].items():
            if attr not in ["id", "name", "label", "x", "y", "z", "size", "width", "height"]:
                node_attributes.add(attr)

                # Track unique values for each attribute
                if attr not in categorical_attributes:
                    categorical_attributes[attr] = set()
                categorical_attributes[attr].add(str(value))

    # Remove attributes with too many unique values (likely numeric)
    categorical_attributes = {k: v for k, v in categorical_attributes.items()
                             if len(v) <= 10 and len(v) > 1}

    logger.info(f"Found potential categorical attributes: {list(categorical_attributes.keys())}")

    return categorical_attributes


def generate_color_mappings(categorical_attributes):
    """
    Generate color mappings for categorical attributes.

    Parameters
    ----------
    categorical_attributes : dict
        Dictionary of categorical attributes and their unique values

    Returns
    -------
    dict
        Dictionary mapping attributes to color dictionaries
    """
    color_mappings = {}
    for attr, values in categorical_attributes.items():
        values_list = list(values)
        palette = generate_color_palette(len(values_list))
        color_mappings[attr] = dict(zip(values_list, palette))
        logger.info(f"Generated color mapping for '{attr}': {color_mappings[attr]}")

    return color_mappings
