# A minimal Dash Cytoscape demonstration
import dash
from dash import html
import dash_cytoscape as cyto
from dash.dependencies import Input, Output

# Initialize the Dash app
app = dash.Dash(__name__, title="Dash Cytoscape Demo")

# Define the elements of the network graph
# In this case, we're creating a simple network with two nodes and one edge
elements = [
    # Nodes
    {'data': {'id': 'node1', 'label': 'Node 1'}},
    {'data': {'id': 'node2', 'label': 'Node 2'}},

    # Edge
    {'data': {'source': 'node1', 'target': 'node2', 'label': 'connects to'}}
]

# Define basic stylesheet for the network
stylesheet = [
    # Style for all nodes
    {
        'selector': 'node',
        'style': {
            'background-color': '#6272A3',  # Node background color
            'label': 'data(label)',         # Use the 'label' field as the node text
            'width': 30,                    # Node width
            'height': 30,                   # Node height
            'text-valign': 'center',        # Vertical alignment of label
            'text-halign': 'center',        # Horizontal alignment of label
            'color': 'white'                # Label text color
        }
    },
    # Style for all edges
    {
        'selector': 'edge',
        'style': {
            'width': 2,                      # Edge width
            'line-color': '#A3627C',         # Edge color
            'target-arrow-color': '#A3627C', # Arrow color
            'target-arrow-shape': 'triangle',# Arrow shape
            'curve-style': 'bezier',         # Edge curve style
            'label': 'data(label)',          # Use the 'label' field for the edge text
            'text-rotation': 'autorotate',   # Auto-rotate text to follow edge
            'text-margin-y': -10,            # Text margin
            'color': '#555'                  # Text color
        }
    }
]

# Define the app layout
app.layout = html.Div([
    html.H1("Dash Cytoscape Network Visualization Demo"),
    html.P("A simple example of a network graph using Dash Cytoscape"),

    # Cytoscape component
    cyto.Cytoscape(
        id='cytoscape-network',
        layout={'name': 'circle'},  # Using circle layout for simplicity
        style={'width': '100%', 'height': '600px'},
        elements=elements,
        stylesheet=stylesheet
    ),

    # Display selected node info
    html.Div(id='selected-node-info', style={'margin-top': '20px'})
])

# Callback to display selected node information
@app.callback(
    Output('selected-node-info', 'children'),
    Input('cytoscape-network', 'tapNodeData')
)
def display_node_info(data):
    """Update the display when a node is clicked"""
    if not data:
        return "No node selected. Click on a node to see its details."

    return f"Selected Node: {data['label']} (ID: {data['id']})"

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
