# Dash Cytoscape Demo

A demonstration project for creating interactive network graphs using Dash and Cytoscape.js.

## Project Overview

This project showcases how to build interactive network visualizations using Dash and the Cytoscape.js library through the dash-cytoscape component.

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
├── README.md            # This documentation
├── pixi.lock            # Lock file for pixi dependencies
├── pyproject.toml       # Python project configuration
└── src                  # Source code directory
    └── dash_cyto_demo   # Main package
        ├── __init__.py  # Package initialization
        └── app.py       # Main application entry point
```

## Usage

Run the application with:

```bash
pixi run python -m dash_cyto_demo.app
```

## Features

- Interactive network visualization
- Node selection and manipulation
- Layout customization
- Data-driven graph rendering

## License

[MIT](LICENSE)
