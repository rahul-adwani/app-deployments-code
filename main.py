import dash
import dash_core_components as dcc
import dash_html_components as html
import flask

# Creating the Layout
server = flask.Flask(__name__)
app = dash.Dash(__name__)
app.title = "Stock Prices"
app.layout = html.Div(children = [html.H1('Stock Visualisation Dashboard')])

if __name__ == '__main__':
    app.run_server(debug=True)
