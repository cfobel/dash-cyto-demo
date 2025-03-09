"""Callback definitions for the Dash Cytoscape dashboard."""

import json
import logging
from dash import html
from dash.dependencies import Input, Output, State

from .styles import get_base_stylesheet, get_color_stylesheet

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def register_callbacks(dash_app):
    """
    Register all callbacks for the dashboard.

    Parameters
    ----------
    dash_app : dash.Dash
        The Dash application instance
    """
    # Callback to display selected node information
    @dash_app.callback(
        Output("selected-node-info", "children"),
        Input("cytoscape-network", "selectedNodeData")
    )
    def display_node_info(data_list):
        """
        Update the display when nodes are selected.

        Parameters
        ----------
        data_list : list
            List of data for all selected nodes

        Returns
        -------
        list
            HTML components representing node information
        """
        if not data_list:
            return "No nodes selected. Click on nodes to see details."

        # Handle multiple selections
        return [
            html.H3(f"Selected Nodes: {len(data_list)}"),
            html.Div([
                html.Div([
                    html.H4(f"Node: {node.get('label', node['id'])}"),
                    html.P(f"ID: {node['id']}"),
                    html.P(f"Properties: {', '.join([f'{k}: {v}' for k, v in node.items() if k != 'id'])}"),
                    html.Hr()
                ]) for node in data_list
            ])
        ]

    @dash_app.callback(
        Output("cytoscape-network", "stylesheet"),
        [Input("color-attr-dropdown", "value")],
        [State("color-mappings-storage", "children")]
    )
    def update_stylesheet(color_attr, color_mappings_json):
        """
        Update the stylesheet when the color attribute changes.

        Parameters
        ----------
        color_attr : str
            Selected attribute to color nodes by
        color_mappings_json : str
            JSON string containing color mappings

        Returns
        -------
        list
            Updated stylesheet
        """
        # Start with the base stylesheet
        updated_style = get_base_stylesheet()

        # If no color attribute is selected, return the basic stylesheet
        if not color_attr:
            return updated_style

        # Parse the color mappings from JSON
        color_mappings = json.loads(color_mappings_json)

        # Add color-specific styles
        updated_style.extend(get_color_stylesheet(color_attr, color_mappings))

        return updated_style

    @dash_app.callback(
        [Output("color-legend", "children"),
         Output("color-legend", "style")],
        [Input("color-attr-dropdown", "value")],
        [State("color-mappings-storage", "children")]
    )
    def update_legend(color_attr, color_mappings_json):
        """
        Update the legend based on the selected color attribute.

        Parameters
        ----------
        color_attr : str
            Selected attribute to color nodes by
        color_mappings_json : str
            JSON string containing color mappings

        Returns
        -------
        tuple
            (legend_content, legend_style)
        """
        # Define the base style for the legend
        legend_style = {
            "margin": "10px 0",
            "padding": "10px",
            "border": "1px solid lightgray",
            "borderRadius": "5px",
        }

        # If no color attribute is selected, hide the legend
        if not color_attr:
            legend_style["display"] = "none"
            return [], legend_style

        # Show the legend
        legend_style["display"] = "block"

        # Parse the color mappings from JSON
        color_mappings = json.loads(color_mappings_json)

        if color_attr not in color_mappings:
            return [html.Div("No legend available for this attribute")], legend_style

        # Create the legend
        legend_items = []
        legend_items.append(html.H4(f"Legend: {color_attr}"))

        for value, color in color_mappings[color_attr].items():
            legend_items.append(html.Div([
                html.Div(style={
                    "display": "inline-block",
                    "width": "20px",
                    "height": "20px",
                    "backgroundColor": color,
                    "marginRight": "10px",
                    "border": "1px solid #ccc"
                }),
                html.Div(value, style={"display": "inline-block"}),
            ], style={"margin": "5px 0"}))

        return legend_items, legend_style

    @dash_app.callback(
        Output("cytoscape-network", "layout"),
        Input("layout-dropdown", "value")
    )
    def update_layout(layout_value):
        """
        Update the Cytoscape layout when dropdown selection changes.

        Parameters
        ----------
        layout_value : str
            Selected layout algorithm name

        Returns
        -------
        dict
            Layout configuration dictionary for Cytoscape
        """
        logger.info(f"Changing layout to: {layout_value}")
        return {"name": layout_value}
