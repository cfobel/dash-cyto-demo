"""A Dash Cytoscape demonstration with Typer CLI."""

import functools
import json
import logging
import random
from pathlib import Path

import dash
import dash_cytoscape as cyto
import networkx as nx
import typer
from dash import html
from dash.dependencies import Input, Output
from networkx.readwrite import cytoscape_data
from networkx.readwrite.json_graph import node_link_data, node_link_graph

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Initialize the Typer app
app_cli = typer.Typer(pretty_exceptions_show_locals=False)

# Create partial functions with explicit edges parameter to avoid deprecation warnings
node_link_data_with_links = functools.partial(node_link_data, edges="links")
node_link_graph_with_links = functools.partial(node_link_graph, edges="links")

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


@app_cli.command()
def generate_sample_graph(
    output_path: Path = typer.Argument(
        ..., help="Output path for the generated NetworkX JSON graph file"
    ),
    nodes: int = typer.Option(10, "--nodes", "-n", help="Number of nodes to generate"),
    max_edges: int = typer.Option(
        3, "--max-edges", "-e", help="Maximum number of outgoing edges per node"
    ),
    directed: bool = typer.Option(
        True,
        "--directed/--undirected",
        help="Whether to create a directed or undirected graph",
    ),
    seed: int = typer.Option(
        None, "--seed", help="Random seed for reproducible graph generation"
    ),
):
    """
    Generate a sample NetworkX graph and save it as JSON.

    Creates a graph with the specified number of nodes and random edges,
    with properties that can be visualized in Dash Cytoscape.
    """
    if seed is not None:
        random.seed(seed)

    # Create a directed or undirected graph
    if directed:
        G = nx.DiGraph()
    else:
        G = nx.Graph()

    # Add nodes with properties
    for i in range(nodes):
        # Generate some sample node properties
        node_properties = {
            "label": f"Node {i}",
            "size": random.randint(1, 10),
            "importance": random.uniform(0, 1),
            "category": random.choice(["A", "B", "C"]),
        }
        G.add_node(i, **node_properties)

    # Add random edges
    for i in range(nodes):
        # Determine number of edges for this node (0 to max_edges)
        num_edges = random.randint(0, min(max_edges, nodes - 1))

        # Get possible targets (excluding self-loops)
        possible_targets = list(range(nodes))
        possible_targets.remove(i)

        if num_edges > 0:
            # Select random targets
            targets = random.sample(
                possible_targets, min(num_edges, len(possible_targets))
            )

            for target in targets:
                # Generate some sample edge properties
                edge_properties = {
                    "label": f"e{i}-{target}",
                    "weight": random.uniform(0.1, 5.0),
                    "type": random.choice(["solid", "dashed", "dotted"]),
                }
                G.add_edge(i, target, **edge_properties)

    # Serialize the graph to JSON using our partial function with explicit edges parameter
    data = node_link_data_with_links(G)

    # Create output directory if it doesn't exist
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Save to file
    with open(output_path, "w") as f:
        json.dump(data, f, indent=2)

    logger.info(
        f"Generated graph with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges"
    )
    logger.info(f"Graph saved to {output_path}")
    logger.info(f"Graph info: {get_graph_info(G)}")

    return G


@app_cli.command()
def run_dashboard(
    graph_path: Path = typer.Argument(
        ...,
        help="Path to NetworkX JSON graph file",
        exists=True,
        dir_okay=False,
        readable=True,
    ),
    debug: bool = typer.Option(False, "--debug", help="Run server in debug mode"),
    port: int = typer.Option(8050, "--port", "-p", help="Port to run the server on"),
    host: str = typer.Option("127.0.0.1", "--host", help="Host to run the server on"),
):
    """
    Run Dash Cytoscape network visualization dashboard from a NetworkX graph.

    This loads a NetworkX graph from a JSON file and visualizes it using Dash Cytoscape.
    All node and edge properties from the NetworkX graph are preserved in the visualization.
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
        raise typer.Exit(1)

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

    # Define basic stylesheet for the network
    stylesheet = [
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
    ]

    # Initialize the Dash app
    dash_app = dash.Dash(__name__, title="Dash Cytoscape Demo")

    # Define the app layout
    dash_app.layout = html.Div(
        [
            html.H1("Dash Cytoscape Network Visualization Demo"),
            html.P(f"Visualizing NetworkX graph from: {graph_path}"),
            # Cytoscape component
            cyto.Cytoscape(
                id="cytoscape-network",
                layout={"name": "circle"},  # Using circle layout for simplicity
                style={"width": "100%", "height": "600px"},
                elements=elements,
                stylesheet=stylesheet,
            ),
            # Display selected node info
            html.Div(id="selected-node-info", style={"margin-top": "20px"}),
        ]
    )

    # Callback to display selected node information
    @dash_app.callback(
        Output("selected-node-info", "children"),
        Input("cytoscape-network", "tapNodeData"),
    )
    def display_node_info(data):
        """
        Update the display when a node is clicked.

        Parameters
        ----------
        data : dict
            Data of the clicked node

        Returns
        -------
        str
            HTML or text representing node information
        """
        if not data:
            return "No node selected. Click on a node to see its details."

        # Display all node properties to show they were preserved
        properties = []
        for key, value in data.items():
            if key != "id":  # Skip ID as it's displayed separately
                properties.append(f"{key}: {value}")

        property_display = (
            ", ".join(properties) if properties else "No additional properties"
        )
        return [
            html.H3(f"Selected Node: {data.get('label', data['id'])}"),
            html.P(f"ID: {data['id']}"),
            html.P(f"Properties: {property_display}"),
        ]

    # Run the app
    logger.info(f"Starting Dash server on {host}:{port}")
    dash_app.run_server(debug=debug, host=host, port=port)


def main():
    """Entry point for the CLI application."""
    app_cli()


if __name__ == "__main__":
    main()
