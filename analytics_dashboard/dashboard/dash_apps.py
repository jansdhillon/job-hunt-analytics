from dash import dcc, html
from dash.dependencies import Input, Output
from django_plotly_dash import DjangoDash

app = DjangoDash('SimpleExample')

app.layout = html.Div([
    dcc.Graph(id='example-graph'),
    dcc.Slider(
        id='slider',
        min=0,
        max=10,
        value=5,
    ),
])

@app.callback(
    Output('example-graph', 'figure'),
    [Input('slider', 'value')]
)
def update_figure(selected_value):
    return {
        'data': [{'x': [1, 2, 3], 'y': [i * selected_value for i in range(1, 4)]}],
        'layout': {'title': f'Graph with multiplier {selected_value}'}
    }
