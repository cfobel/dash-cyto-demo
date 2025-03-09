"""Dashboard module for Dash Cytoscape visualization."""

import json
import logging
from pathlib import Path

import dash
import dash_cytoscape as cyto
from networkx.readwrite import cytoscape_data

from ..graph_utils import node_link_graph_with_links, get_graph_info, extract_categorical_attributes, generate_color_mappings
from .layout import create_dashboard_layout
from .callbacks import register_callbacks

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Load extra Cytoscape.js layouts
cyto.load_extra_layouts()

def run_dashboard(
    graph_path: Path,
    layout: str = "circle",
    color_by: str = None,
    debug: bool = False,
    host: str = "127.0.0.1",
    port: int = 8050,
):
    """
    Run Dash Cytoscape network visualization dashboard from a NetworkX graph.

    This loads a NetworkX graph from a JSON file and visualizes it using Dash Cytoscape.
    All node and edge properties from the NetworkX graph are preserved in the visualization.

    Parameters
    ----------
    graph_path : Path
        Path to NetworkX JSON graph file
    layout : str
        Initial Cytoscape layout algorithm
    color_by : str
        Node attribute to use for categorical coloring
    debug : bool
        Run server in debug mode
    host : str
        Host to run the server on
    port : int
        Port to run the server on
    """
    # Load NetworkX graph from JSON
    logger.info(f"Loading graph from {graph_path}")
    try:
        with open(graph_path, "r") as f:
            graph_data = json.load(f)
        # Use the partial function with explicit edges parameter
        graph = node_link_graph_with_links(graph_data)
        logger.info(f"Graph loaded: {get_graph_info(graph)}")
    except Exception as e:
        logger.error(f"Failed to load graph: {e}")
        raise ValueError(f"Failed to load graph: {e}")

    # Convert NetworkX graph to Cytoscape format using built-in function
    cyto_data = cytoscape_data(graph)

    # Log node and edge properties to demonstrate preservation
    for node in cyto_data["elements"]["nodes"]:
        logger.info(f"Node {node['data'].get('id')} properties: {node['data']}")

    for edge in cyto_data["elements"].get("edges", []):
        logger.info(
            f"Edge {edge['data'].get('source')}->{edge['data'].get('target')} properties: {edge['data']}"
        )

    # Extract elements list for Cytoscape
    elements = []
    elements.extend(cyto_data["elements"]["nodes"])
    if "edges" in cyto_data["elements"]:
        elements.extend(cyto_data["elements"]["edges"])

    # Get categorical attributes that could be used for coloring
    categorical_attributes = extract_categorical_attributes(cyto_data)

    # Define the initial color_by attribute
    initial_color_attr = None
    if color_by is not None and color_by in categorical_attributes:
        initial_color_attr = color_by
    elif categorical_attributes:
        initial_color_attr = list(categorical_attributes.keys())[0]

    # Create color mappings for each attribute
    color_mappings = generate_color_mappings(categorical_attributes)

    # Initialize the Dash app
    dash_app = dash.Dash(__name__, title="Dash Cytoscape Demo")

    # Set the app layout
    dash_app.layout = create_dashboard_layout(
        elements=elements,
        graph_path=graph_path,
        initial_layout=layout,
        categorical_attributes=categorical_attributes,
        initial_color_attr=initial_color_attr,
        color_mappings=color_mappings
    )

    # Register callbacks
    register_callbacks(dash_app)

    # Run the app
    logger.info(f"Starting Dash server on {host}:{port}")
    dash_app.run_server(debug=debug, host=host, port=port)
