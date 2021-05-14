# run by cd path/where/this/file/script/exists
# python3 barplot_311.py 

import plotly.express as px
import plotly.io as pio
import plotly.graph_objects as go
from plotly.subplots import make_subplots
pio.templates.default = "plotly_dark"

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd
import os



# load your data
BASE_DIR = "/Users/karinalopez/Desktop/ds_projects/hack4la_311/scripts/interactive/"
os.chdir(BASE_DIR)
df = pd.read_csv('distribution_requests_by_date_cd.csv')


# Get checklist options
all_cd = df.cd.unique()


# idk what this does; prepare your app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets = external_stylesheets)

# create your app layout
app.layout = html.Div([
    
    # create your checklist button for council district selection
    dcc.Dropdown(
        
        id = "dropdown",
        
        options = [{"label": x, "value": x} 
                 for x in all_cd],
        
        value = all_cd[0],
        multi = False,
        placeholder = "Select a council district in Los Angeles County"
        
    ),
    
    # create your button for 
    
    
    dcc.Graph(id = "scatter"),
    
])


# Setup callback function
@app.callback(
    Output("scatter", "figure"), 
    [Input("dropdown", "value")])



# Plot your PPP loan comparison by income group based on user input
def update_line_chart(cd):
    
    # create your mask filter
    temp = df.loc[df['cd'] == cd]
    
    # filter by month and year as well
    temp = temp.loc[df['created_month'] == 'January']
    temp = temp.loc[df['created_year'] == 2020]
    
         
    # Create figure with secondary y-axis
    fig = make_subplots(specs = [[{"secondary_y": True}]])

    # Add traces
    fig.add_trace(
        go.Bar(x = temp['requesttype'], y = temp['count_service'], name = "Number of requests"),
        secondary_y = False,
    )

    fig.add_trace(
        go.Scatter(x = temp['requesttype'], y = temp['percentage_service'], name = "Percentage"),
        secondary_y = True,
    )

    # Add figure title
    fig.update_layout(
        title_text = "Count of services requested for this district"
    )

    # Set x-axis title
    fig.update_xaxes(title_text = "Service Request")

    # Set y-axes titles
    fig.update_yaxes(title_text="<b>Count</b>", secondary_y = False)
    fig.update_yaxes(title_text="<b>Percent</b>", secondary_y=True)

 
    return fig


# Run your dash app
if __name__ == '__main__':
    app.run_server(debug = True)











