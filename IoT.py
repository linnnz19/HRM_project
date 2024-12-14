import dash
from dash import dcc, html
import random

# Initialize Dash app
app = dash.Dash()

# Simulate IoT sensor data (0 = no helmet, 1 = helmet on)
def sensor_data():
    return 1 if random.random() < 0.7 else 0  # 70% chance of wearing a helmet, 30% of not wearing

# Generate the worker light indicators based on safety statuses
def get_lights(worker_ids, safety_statuses):
    lights = []
    for worker_id, status in zip(worker_ids, safety_statuses):
        color = 'green' if status == 1 else 'red'  # Green for wearing helmet, Red for no helmet
        lights.append(
            html.Div(
                children=[
                    html.Div(f"{worker_id}", style={'textAlign': 'center', 'marginTop': '10px'}),
                    html.Div(
                        style={
                            'width': '50px',
                            'height': '50px',
                            'borderRadius': '50%',
                            'backgroundColor': color,
                            'margin': '10px auto'
                        }
                    )
                ],
                style={'display': 'inline-block', 'width': '80px', 'textAlign': 'center', 'margin': '10px'}
            )
        )
    return lights

# Layout of the app
app.layout = html.Div([
    # Worker status lights display
    html.Div(id='worker_lights', children=[], style={'display': 'flex', 'flexWrap': 'wrap', 'justifyContent': 'center'}),

    # Display for workers not wearing helmets
    html.Div(id='no_helmet_workers', children=[], style={'textAlign': 'center', 'marginTop': '20px', 'fontSize': '20px', 'fontWeight': 'bold'}),

    # Danger rate display
    html.Div(id='danger_rate', children=[], style={'textAlign': 'center', 'marginTop': '20px', 'fontSize': '20px', 'fontWeight': 'bold'}),

    # Interval component to update every 5 seconds
    dcc.Interval(id='interval-component', interval=5000, n_intervals=0)  # Update every 5 seconds
])

# Callback to update the lights, list no-helmet workers, and calculate danger rate
@app.callback(
    [dash.dependencies.Output('worker_lights', 'children'),
     dash.dependencies.Output('no_helmet_workers', 'children'),
     dash.dependencies.Output('danger_rate', 'children')],
    dash.dependencies.Input('interval-component', 'n_intervals')
)
def update_lights(n):
    worker_ids = [f"Worker {i+1}" for i in range(20)]  # 20 worker IDs
    safety_statuses = [sensor_data() for _ in worker_ids]  # Simulated sensor data (70% chance of helmet)
    
    # Get the lights for each worker
    lights = get_lights(worker_ids, safety_statuses)
    
    # List workers who are not wearing helmets
    no_helmet_workers = [worker_ids[i] for i in range(len(safety_statuses)) if safety_statuses[i] == 0]
    no_helmet_text = f"Workers not wearing helmets: {', '.join(no_helmet_workers)}" if no_helmet_workers else "All workers are wearing helmets."
    
    # Calculate the danger rate
    danger_rate = (len(no_helmet_workers) / len(worker_ids)) * 100
    danger_rate_text = f"Danger rate: {danger_rate:.2f}%"

    return lights, no_helmet_text, danger_rate_text

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)
