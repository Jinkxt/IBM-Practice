# Import required packages
import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc
from dash.dependencies import Input, Output

# Read the airline data into pandas dataframe
airline_data =  pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/airline_data.csv', 
                            encoding = "ISO-8859-1",
                            dtype={'Div1Airport': str, 'Div1TailNum': str, 
                                   'Div2Airport': str, 'Div2TailNum': str})

# Randomly sample 500 data points. Setting the random state to be 42 so that we get same result.
data = airline_data.sample(n=500, random_state=42)

# Pie Chart Creation
fig = px.sunburst(data, path=['Month', 'DestStateName'], values='Flights', names='DistanceGroup', title='Distance group proportion by flights')

# Create a dash application
app = Dash(__name__)


fig2 = px.sunburst(data, path=['Month', 'DestStateName'], values='Flights', names='DistanceGroup', title='Distance group proportion by flights')



@app.callback(Output(component_id='Airline_Performance_Dashboard_Figure', component_property='figure'),
              Input(component_id='input-yr2', component_property='value'))
def get_grapsh(Year):
    avgarrdelay_month=data.loc[data['Year']==Year].groupby('Month')['ArrDelay'].mean().to_frame().reset_index()
    fig3 = px.line(avgarrdelay_month, x='Month', y='ArrDelay', title='Average flight arrival delay per month' , labels={'Month': 'Month', 'ArrDelay': 'Average Arrival Delay'})
    fig3.update_layout()
    return fig3


# Get the layout of the application and adjust it.
# Create an outer division using html.Div and add title to the dashboard using html.H1 component
# Add description about the graph using HTML P (paragraph) component
# Finally, add graph component.
app.layout = html.Div(children=[html.H1("Learning about dash interactive dashboards"),
                                
                                html.P("This time we will be setting a flask server to host our dash app which contains some plotly graphs"),
                                html.Div([html.Div([
                                                    html.H2("Testing first graphics"),
                                                    html.P("Random plotly sunburst"),
                                                    dcc.Graph(figure=fig)
                                                    ],
                                                    style={
                                                        'width': '50%',
                                                       'float': 'left'
                                                    }),
                                          html.Div([
                                                    html.H2("Handling inputs outputs using python decorator "),
                                                    html.P("As an example let's use the input parameters to update a plotly graph"),
                                                    html.P("We need an html element to capture the input , let's go with a div"),
                                                    html.Div(['Input: ', dcc.Input(id='input-yr', value=2010, type='number')]),
                                                    dcc.Graph(figure=fig2)
                                                   ],
                                                   style={
                                                       'width': '50%',
                                                       'float': 'left'
                                                   })],
                                         style={
                                                'padding': '20px',
                                                }),
                                html.Div(id='Airline_Performance_Dashboard', children=[
                                        html.H1('Airline Performance Dashboard', style={'text-align':'center'}),
                                        html.Div(['Input Year: ', dcc.Input(id='input-yr2', value=2010, type='number')]),
                                        dcc.Graph(id='Airline_Performance_Dashboard_Figure') 
                                ])
                               ])

# Run the application                   
if __name__ == '__main__':
    app.run(host='127.0.0.1',    port='45566',)
