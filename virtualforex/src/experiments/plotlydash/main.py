import dash
from dash import dcc, html, Input, Output, State
import plotly.graph_objects as go
import pandas as pd

# Incorporate data
# df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv')
df = pd.read_csv("G:\\My Drive\\data\\MetaTrader5\\EURUSDDaily.csv", parse_dates=['Date'])

# Function to build the figure with markers
def create_figure(markers=[]):
    fig = go.Figure(data=[go.Candlestick(
        x=df['Date'],
        open=df['Open'],
        high=df['High'],
        low=df['Low'],
        close=df['Close']
    )])
    fig.update_layout(
        height=700,
        xaxis_rangeslider_visible=True,
        yaxis_fixedrange=False,
        title="Click to place Buy/Sell markers"
    )
    # Add markers (buy/sell as scatter points)
    for m in markers:
        fig.add_trace(go.Scatter(
            x=[m['x']],
            y=[m['y']],
            mode='markers+text',
            marker=dict(
                color='green' if m['type'] == 'Buy' else 'red',
                size=12,
                symbol='triangle-up' if m['type'] == 'Buy' else 'triangle-down'
            ),
            text=[m['type']],
            textposition='top center' if m['type'] == 'Buy' else 'bottom center',
            name=m['type'],
            showlegend=False
        ))
    return fig

# Global state for placed markers
markers = []

# Initialize Dash app
app = dash.Dash(__name__)
app.layout = html.Div([
    html.Div([
        html.Button("Buy", id="buy-button", n_clicks=0),
        html.Button("Sell", id="sell-button", n_clicks=0),
        html.Div(id="selected-action", children="No action selected"),
    ], style={"marginBottom": "20px"}),

    dcc.Graph(id="candlestick-chart", figure=create_figure()),

    # Hidden store to keep track of selected action
    dcc.Store(id='current-action', data=None)
])

# Handle Buy/Sell button clicks
@app.callback(
    Output('current-action', 'data'),
    Output('selected-action', 'children'),
    Input('buy-button', 'n_clicks'),
    Input('sell-button', 'n_clicks'),
    prevent_initial_call=True
)
def update_action(buy_clicks, sell_clicks):
    ctx = dash.callback_context
    if not ctx.triggered:
        raise dash.exceptions.PreventUpdate

    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    if button_id == "buy-button":
        return "Buy", "Selected: Buy"
    elif button_id == "sell-button":
        return "Sell", "Selected: Sell"

# Handle click on chart to place marker
@app.callback(
    Output("candlestick-chart", "figure"),
    Input("candlestick-chart", "clickData"),
    State("current-action", "data"),
)
def place_marker(clickData, action):
    global markers
    if clickData and action:
        x = clickData['points'][0]['x']
        y = clickData['points'][0]['y']
        markers.append({'x': x, 'y': y, 'type': action})
    return create_figure(markers)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
