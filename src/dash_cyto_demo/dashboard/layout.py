"""Layout definitions for the Dash Cytoscape dashboard."""

import json
import dash_cytoscape as cyto
from dash import html, dcc

def get_available_layouts():
    """
    Get a list of available Cytoscape layouts.

    Returns
    -------
    list
        List of layout names
    """
    return [
        # Default layouts
        "circle", "grid", "random", "concentric",
        "breadthfirst", "cose", "null",
        # Extra layouts (require cyto.load_extra_layouts())
        "dagre", "klay", "euler", "spread", "cose-bilkent"
    ]


def create_dashboard_layout(elements, graph_path, initial_layout, categorical_attributes, initial_color_attr, color_mappings):
    """
    Create the layout for the dashboard.

    Parameters
    ----------
    elements : list
        List of elements (nodes and edges) for Cytoscape
    graph_path : Path
        Path to the graph file
    initial_layout : str
        Initial layout algorithm to use
    categorical_attributes : dict
        Dictionary of categorical attributes and their values
    initial_color_attr : str
        Initial attribute to color nodes by
    color_mappings : dict
        Dictionary mapping attributes to color dictionaries

    Returns
    -------
    dash.html.Div
        Main layout component for the dashboard
    """
    # Get available layouts
    available_layouts = get_available_layouts()

    # Ensure the provided layout is valid
    if initial_layout not in available_layouts:
        initial_layout = "circle"

    return html.Div(
        [
            html.H1("Dash Cytoscape Network Visualization Demo"),
            html.P(f"Visualizing NetworkX graph from: {graph_path}"),

            # Layout and color settings div
            html.Div([
                # Layout selection dropdown
                html.Div([
                    html.Label("Select Layout:"),
                    dcc.Dropdown(
                        id="layout-dropdown",
                        options=[{"label": l.capitalize(), "value": l} for l in available_layouts],
                        value=initial_layout,  # Use the layout from CLI parameter as default
                        clearable=False,
                        style={"width": "200px"}
                    )
                ], style={"display": "inline-block", "marginRight": "20px"}),

                # Node color attribute dropdown (only if categorical attributes exist)
                html.Div([
                    html.Label("Color Nodes By:"),
                    dcc.Dropdown(
                        id="color-attr-dropdown",
                        options=[{"label": attr, "value": attr} for attr in categorical_attributes.keys()],
                        value=initial_color_attr,
                        clearable=True,
                        placeholder="Select attribute...",
                        style={"width": "200px"}
                    )
                ], style={"display": "inline-block"}) if categorical_attributes else None,
            ], style={"margin": "10px 0"}),

            # Legend div
            html.Div(
                id="color-legend",
                style={
                    "margin": "10px 0",
                    "padding": "10px",
                    "border": "1px solid lightgray",
                    "borderRadius": "5px",
                    "display": "none" if not initial_color_attr else "block"
                }
            ),

            # Cytoscape component
            cyto.Cytoscape(
                id="cytoscape-network",
                layout={"name": initial_layout},
                style={"width": "100%", "height": "600px"},
                elements=elements,
                boxSelectionEnabled=True,
                autounselectify=False,
            ),

            # Display selected node info
            html.Div(id="selected-node-info", style={"margin-top": "20px"}),

            # Store the color mappings in a hidden div
            html.Div(id="color-mappings-storage", style={"display": "none"},
                     children=json.dumps(color_mappings))
        ]
    )
