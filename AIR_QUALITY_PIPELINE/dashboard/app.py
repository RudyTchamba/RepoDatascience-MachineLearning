import dash
from dash import dcc, html, Input, Output
import plotly.express as px # This the library that contains the visual componets that will be added to dash
import duckdb
import pandas as pd

with duckdb.connect("../air_quality.db", read_only=True) as db_connection:
    df = db_connection.execute(
        "SELECT * FROM presentation.air_quality_data"
    ).fetchdf()

    daily_stats_df = db_connection.execute(
        "SELECT * FROM presentation.daily_air_quality_stats"
    ).fetchdf()

    latest_values_df = db_connection.execute(
        "SELECT * FROM presentation.latest_param_values_per_location"
    ).fetchdf()


def map_figure():
    
    map_fig = px.scatter_mapbox(
        latest_values_df,
        lat="lat",
        Lon="lon",
        hover_name="location",
        hover_data={
            """"lat": False,
            "lon": False,"""
            "datetime":True,
            "pm10": True,
            "pm25": True,
            "so2": True
        },
        zoom=6.0
    )

    map_fig.update_layout(
        mapbox_style = "open-street-map",
        height=1000,
        title="Air Quality Monitoring Locations"
    )

    return map_fig

app = dash.Dash(__name__)

app.layout = html.Div(
    dcc.Graph(id="Sensor Locations", figure=map_figure)
)

if __name__ == "__main__":
    app.run_server(debug=True)