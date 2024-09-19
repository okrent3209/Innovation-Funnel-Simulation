import dash
from dash import dcc, html
import plotly.graph_objs as go
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

# Set up the layout
app.layout = html.Div([
    html.H1("Innovation Funnel Simulation"),
    
    # Idea Generation Rate Slider
    html.Label("Idea Generation Rate"),
    dcc.Slider(id='idea-generation-rate', min=0, max=100, step=1, value=50, 
               marks={i: f'{i}' for i in range(0, 101, 10)}),
    
    # Screening Rigidity Slider
    html.Label("Screening Rigidity (%)"),
    dcc.Slider(id='screening-rigidity', min=0, max=100, step=1, value=30, 
               marks={i: f'{i}%' for i in range(0, 101, 10)}),
    
    # Development Speed Slider
    html.Label("Development Speed (Months)"),
    dcc.Slider(id='development-speed', min=1, max=12, step=1, value=6, 
               marks={i: f'{i}' for i in range(1, 13)}),
    
    # Success Rate Slider
    html.Label("Market Success Rate (%)"),
    dcc.Slider(id='success-rate', min=0, max=100, step=1, value=50, 
               marks={i: f'{i}%' for i in range(0, 101, 10)}),
    
    # Funnel Visualization
    dcc.Graph(id='funnel-chart'),
    
    # Display success chance
    html.Div(id='success-output')
])

# Define the callback to update the funnel chart and calculate success probability
@app.callback(
    [Output('funnel-chart', 'figure'),
     Output('success-output', 'children')],
    [Input('idea-generation-rate', 'value'),
     Input('screening-rigidity', 'value'),
     Input('development-speed', 'value'),
     Input('success-rate', 'value')]
)
def update_funnel(idea_rate, screening_rigidity, dev_speed, success_rate):
    # Simulate data
    total_ideas = idea_rate
    screened_ideas = total_ideas * (1 - screening_rigidity / 100)
    developed_ideas = screened_ideas * (12 / dev_speed)  # Faster development leads to more successful ideas
    
    # Final number of successful products
    successful_products = developed_ideas * (success_rate / 100)
    
    # Create funnel data
    funnel_data = [total_ideas, screened_ideas, developed_ideas, successful_products]
    funnel_labels = ["Idea Generation", "Screening", "Development", "Market Success"]
    
    # Create a funnel chart
    fig = go.Figure(go.Funnel(
        y=funnel_labels,
        x=funnel_data
    ))
    
    # Success probability text
    success_message = f"Estimated Successful Products: {successful_products:.2f}"
    
    return fig, success_message

if __name__ == '__main__':
    app.run_server(debug=True)
