# Dash Cytoscape Demo

A demonstration project for creating interactive network graphs using Dash and Cytoscape.js.

## Project Overview

This project showcases how to build interactive network visualizations using Dash and the Cytoscape.js library through the dash-cytoscape component. It provides both a command-line interface for generating sample graphs and a visualization dashboard for exploring network data.

## Installation

### Using pixi

This project uses [pixi](https://github.com/prefix-dev/pixi) for environment management:

```bash
# Install pixi if you haven't already
curl -fsSL https://pixi.sh/install.sh | bash

# Install dependencies
pixi install
```

## Project Structure

```
├── README.md                      # This documentation
├── pixi.lock                      # Lock file for pixi dependencies
├── pyproject.toml                 # Python project configuration
└── src                            # Source code directory
    └── dash_cyto_demo             # Main package
        ├── __init__.py            # Package initialization
        ├── app.py                 # CLI entry point with Typer
        ├── graph_generator.py     # Graph generation utilities
        ├── graph_utils.py         # NetworkX utility functions
        └── dashboard              # Dashboard package
            ├── __init__.py        # Dashboard initialization
            ├── callbacks.py       # Dash callbacks
            ├── layout.py          # Dashboard layout definition
            └── styles.py          # Stylesheet and visual styling
```

## Usage

### Generating Sample Graphs

Create a sample NetworkX graph with configurable properties:

```bash
pixi run python -m dash_cyto_demo.app generate-sample-graph output.json --nodes 20 --max-edges 5
```

Options:
- `--nodes`: Number of nodes to generate (default: 10)
- `--max-edges`: Maximum outgoing edges per node (default: 3)
- `--directed/--undirected`: Create directed or undirected graph (default: directed)
- `--seed`: Random seed for reproducible generation

### Running the Dashboard

Visualize an existing graph stored in JSON format:

```bash
pixi run python -m dash_cyto_demo.app run-dashboard path/to/graph.json
```

Options:
- `--layout`: Initial layout algorithm (default: circle)
- `--color-by`: Node attribute to use for categorical coloring
- `--debug`: Run in debug mode
- `--port`: Port to run on (default: 8050)
- `--host`: Host to listen on (default: 127.0.0.1)

## Features

- Interactive network visualization
- Multiple layout algorithms
- Node coloring by categorical attributes
- Node selection and multi-selection
- Dynamic filtering and highlighting
- Command-line interface for graph generation
- JSON import/export for NetworkX graphs

## License

[MIT](LICENSE)
