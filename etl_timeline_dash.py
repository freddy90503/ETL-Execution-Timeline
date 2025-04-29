import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html, Input, Output

# Load your CSV file
csv_path = "VisualDataTime.csv"
df = pd.read_csv(csv_path)

# Convert time strings to datetime (with dummy date)
df['Start Timestamp'] = pd.to_datetime(df['Start Time'], format="%I:%M %p")
df['End Timestamp'] = pd.to_datetime(df['End Time'], format="%I:%M %p")

# Create Gantt-style timeline
fig = px.timeline(df, x_start="Start Timestamp", x_end="End Timestamp", y="ETL", color="ETL")
fig.update_yaxes(autorange="reversed")
fig.update_layout(
    xaxis_title="Time of Day (CST)",
    yaxis_title="ETL",
    height=800,
    font=dict(size=14),
    xaxis=dict(
        tickformat="%H:%M",
        tickangle=0,
        title_font=dict(size=16),
    ),
    yaxis=dict(title_font=dict(size=16)),
    title_font=dict(size=20)
)

# Dash app
app = dash.Dash(__name__)
app.layout = html.Div([
    html.H1("Interactive ETL Execution Timeline"),
    dcc.Input(id='etl-search', type='text', placeholder='Search ETL name...'),
    dcc.Graph(id='etl-timeline', figure=fig)
])

@app.callback(
    Output('etl-timeline', 'figure'),
    Input('etl-search', 'value')
)
def update_figure(search_value):
    filtered_df = df[df['ETL'].str.contains(search_value, case=False)] if search_value else df
    fig = px.timeline(filtered_df, x_start="Start Timestamp", x_end="End Timestamp", y="ETL", color="ETL")
    fig.update_yaxes(autorange="reversed")
    fig.update_layout(
        title="ETL Execution Timeline (Filtered)",
        xaxis_title="Time of Day (CST)",
        height=800,
        font=dict(size=14),
        xaxis=dict(tickformat="%H:%M"),
        title_font=dict(size=20)
    )
    return fig

if __name__ == '__main__':
    app.run(debug=True)