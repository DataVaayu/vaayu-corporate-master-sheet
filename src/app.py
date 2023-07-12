import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import callback, dcc, Input, Output, html, Dash

#load the data
vaayu_corporate_master = pd.read_csv("VAAYU CORPORATE MASTER SHEET_ ANJI - DATA DUMP.csv")

#make the week of month column
vaayu_corporate_master["Week of Month"] = pd.to_datetime(vaayu_corporate_master["DATE"]).dt.day.apply(lambda x: (x-1)//7 +1)
vaayu_corporate_master["Week of Month"] = vaayu_corporate_master["Week of Month"].apply(lambda x: "Week " + str(x))
vaayu_corporate_master["DATE"]=pd.to_datetime(vaayu_corporate_master["DATE"])
vaayu_corporate_master["Month Name"]=vaayu_corporate_master["DATE"].dt.month_name()

# fill blank values
vaayu_corporate_master.fillna("no data",inplace=True)
print(vaayu_corporate_master.isnull().sum())
# building the application

app = Dash(__name__)
server=app.server

app.layout = html.Div([
    html.H1("Analysis of Corporate Master Sheet - Vaayu"),
    html.Div(children=[
        html.H2("Choose Parameters from Dropdown"),
        dcc.Dropdown(id="columns-dropdown-1",value=["Month Name","Week of Month"],options=vaayu_corporate_master.columns,multi=True),
        dcc.Graph(id="treemap-1"),
        
    ],style={"padding":10,"flex":1})   
    
])

@callback(
    Output("treemap-1","figure"),
    Input("columns-dropdown-1","value")
)

def update_graph(value1):
    path=value1
    fig=px.treemap(vaayu_corporate_master,path=path,height=700,width=1000)
    fig.update_traces(textinfo="label+value")
    
    return fig

if __name__ == '__main__':
    app.run(debug=True)
