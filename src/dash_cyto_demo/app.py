"""A Dash Cytoscape demonstration with Typer CLI."""

import logging
from pathlib import Path

import typer

# Import from our refactored modules
from .graph_generator import generate_sample_graph
from .dashboard import run_dashboard

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Initialize the Typer app
app_cli = typer.Typer(pretty_exceptions_show_locals=False)

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
    from .graph_generator import generate_sample_graph as gen_graph
    return gen_graph(
        output_path=output_path,
        nodes=nodes,
        max_edges=max_edges,
        directed=directed,
        seed=seed
    )


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
    layout: str = typer.Option("circle", "--layout", "-l", help="Initial Cytoscape layout algorithm"),
    color_by: str = typer.Option(None, "--color-by", "-c", help="Node attribute to use for categorical coloring"),
):
    """
    Run Dash Cytoscape network visualization dashboard from a NetworkX graph.

    This loads a NetworkX graph from a JSON file and visualizes it using Dash Cytoscape.
    All node and edge properties from the NetworkX graph are preserved in the visualization.
    """
    from .dashboard import run_dashboard as run_dash
    run_dash(
        graph_path=graph_path,
        layout=layout,
        color_by=color_by,
        debug=debug,
        host=host,
        port=port
    )


def main():
    """Entry point for the CLI application."""
    app_cli()


if __name__ == "__main__":
    main()
