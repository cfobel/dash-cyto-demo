"""Functions for generating sample graphs."""

import json
import random
import logging
import networkx as nx
from pathlib import Path

from .graph_utils import node_link_data_with_links, get_graph_info

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def generate_sample_graph(
    output_path: Path,
    nodes: int = 10,
    max_edges: int = 3,
    directed: bool = True,
    seed: int = None,
):
    """
    Generate a sample NetworkX graph and save it as JSON.

    Creates a graph with the specified number of nodes and random edges,
    with properties that can be visualized in Dash Cytoscape.

    Parameters
    ----------
    output_path : Path
        Output path for the generated NetworkX JSON graph file
    nodes : int
        Number of nodes to generate
    max_edges : int
        Maximum number of outgoing edges per node
    directed : bool
        Whether to create a directed or undirected graph
    seed : int
        Random seed for reproducible graph generation

    Returns
    -------
    networkx.Graph
        The generated graph
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
