#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas_datareader.data as web
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from datetime import datetime as dt


# In[2]:


# Creating the Layout
app = dash.Dash(__name__)
#app = app.server
app.title = "Stock Prices"
app.layout = html.Div(children = [
    html.H1('Stock Visualisation Dashboard'),
    html.H4('Please enter the stock name'),
    dcc.Input(id="input", value="", type="text"),
    html.Div(id="output-graph")
])


# In[3]:


# Creating User Interaction Handlers
@app.callback(
    Output(component_id="output-graph", component_property="children"),
    [Input(component_id="input", component_property="value")]
)
def update_value(input_data):
    start_date = dt(2010, 1, 13)
    end_date = dt.now()
    df = web.DataReader(input_data, 'yahoo', start_date, end_date)
    return dcc.Graph(id="demo", figure={'data':[{'x':df.index, 'y':df.Close, 'type':'line', 'name':input_data}, ],
                                        'layout':{'title':input_data}})


# In[ ]:


if __name__ == "__main__":
    app.run_server(host='0.0.0.0', port=8081, debug=True)

