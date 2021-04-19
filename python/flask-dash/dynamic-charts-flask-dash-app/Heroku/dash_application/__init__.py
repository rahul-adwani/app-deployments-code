import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output, State

def create_dash_application(flask_app):
    dash_app = dash.Dash(server=flask_app, name="Dashboard", url_base_pathname="/dash")
    item1 = html.Div(
    [
        html.P("Welcome to the Stock Dash App!!", className="Start"),
        html.Div(
        [
            html.P("Input Stock Code:", className="Heading"),
            html.Tr([
                html.Td([
                    #stock code input
                    dcc.Input(
                    id="stock_code".format("text"),value='AAPL',
                    placeholder="".format("text"),
                    )
                ]),
                html.Td([
                    #submit button
                    html.Button(
                    'Submit', id="codesubmit",
                    className="item1inputs", n_clicks=0
                    )
                ])
            ])
        ]),
        html.Br(),
        html.Br(),
        html.Div([
            #Date Range Picker Input
            dcc.DatePickerRange(
            id='my-date-picker-range',
            min_date_allowed=dt(2019, 8, 5),
            max_date_allowed=dt(2020, 9, 19),
            initial_visible_month=dt(2020, 8, 5),
            end_date=dt(2020, 8, 25)
            ),
        ]),
        html.Br(),
        html.Div([
        
            html.Tr([
                html.Td([
                    #Stock Price Button
                    html.Button(
                    'Stock Price',
                    className="inputs"
                    ),
                ]),
                html.Td([
                    #Indicators Button
                    html.Button(
                    'Indicators', id="indicatorBtn", n_clicks=0,
                    className="inputs"
                    )
                ])
            ]),
            html.Br(),
        
            #No of days of Forecast Input
            dcc.Input(
            id="number_of_days".format("number"),
            placeholder="number of days".format("number"),
            ),
            #Forecast Button
            html.Button(
            'Forecast',
            className="inputs"
            ),
        ]),
    ],
    className="nav"
    )

    item2 = html.Div(
    [
        html.Div([
            #Logo
            html.Div([
            html.Img(id="cologo"),
            ]),
            #Company Name
            html.P(id="coname", className="Start"),
        ], className="header"),
        html.Div([
            #Description
            ], id="description", className="decription_ticker"),
        html.Div([
            # Stock price plot
            dcc.Graph(responsive=True, id="graphs-content", className="graph_cls")
            ]),
        html.Div([
                # Indicator plot
            ], id="main-content"),
        html.Div([
                # Forecast plot
            ], id="forecast-content")
          ],
        className="content")

    @dash_app.callback([
        Output("description", "children"),
        Output("cologo", "src"),
        Output("coname", "children"),
        Input("codesubmit","n_clicks"),
        State("stock_code", "value")])
    def update_data(arg1, arg2):
        #return arg1, arg1, arg1
        ticker = yf.Ticker(arg2)
        inf = ticker.info
        df = pd.DataFrame().from_dict(inf, orient="index").T
        return df['longBusinessSummary'][0], df['logo_url'][0], df['shortName'][0]
        
    @dash_app.callback(
        Output("graphs-content","figure"),
        [Input("my-date-picker-range", "start_date"),
        Input("my-date-picker-range", "end_date"),
        Input("stock_code", "value"),
        State("codesubmit", "n_clicks")])
    def plot_graph(arg1, arg2, arg3, arg4):
        #return arg1, arg1, arg1
        df = yf.download(arg3,arg1,arg2)
        df.reset_index(inplace=True)
        fig = get_stock_price_fig(df)
        return fig
    def get_stock_price_fig(df):
        colors = px.colors.qualitative.Plotly
        fig = go.Figure()
        fig.add_traces(go.Scatter(x=df['Date'], y = df['Open'], mode = 'lines', line=dict(color=colors[0])))
        fig.add_traces(go.Scatter(x=df['Date'], y = df['Close'], mode = 'lines', line=dict(color=colors[1])))
        return fig
    


    dash_app.layout = html.Div([item1, item2], className="container")
    
    return dash_app

if __name__ == '__main__':
    app.run_server(debug=True)