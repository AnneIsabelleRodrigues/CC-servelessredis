from dash import Dash, html, dcc, dash_table
import plotly.express as px
import pandas as pd
import redis
import json

redis_host = '192.168.121.66'  
redis_port = 6379 
redis_client = redis.StrictRedis(host=redis_host, port=redis_port, decode_responses=True)

redis_key = 'annecarvalho-proj3-output'

data_json = redis_client.get(redis_key)

if data_json:
    data_dict = json.loads(data_json)

df = pd.DataFrame([data_dict])

df = df.transpose()
df.reset_index(inplace=True)
df.columns = ['index', 'value']

app = Dash(__name__)

app.layout = html.Div([
    dcc.Interval(id='Interval', interval=1000),
    html.H1(children='Cloud Computing - Real Time Data from Redis', style={'textAlign':'center', 'color': '#b41c2c'}),
    html.H3(children=f'Última Atualização: {df.iloc[0][1]}', style={'textAlign':'center', 'color': '#b41c2c'}),
    dash_table.DataTable(
    style_as_list_view=True,
    style_cell={'padding': '5px'},
    style_header={
        'backgroundColor': 'white',
        'fontWeight': 'bold',
        'color': '#b41c2c'
    },
    data=df[1:].to_dict('records'),
    fixed_columns={'headers': True, 'data': 2},
    style_table={'maxWidth': '60%','textAlign': 'center',
            "margin-left":"30%",
            "margin-right":"20%"}),
    html.H4(children='Average Utilization', style={'textAlign':'center'}),
    dcc.Graph(figure=px.bar(df[4:], x='index', y='value', color_discrete_sequence=px.colors.sequential.RdBu)),
    html.H4(children='Network Egress (%)', style={'textAlign':'center'}),
    dcc.Graph(figure=px.pie(df[1:2], values=[df.iloc[1][1], 100 - df.iloc[1][1]], names=[df.iloc[1][0], '-'], color_discrete_sequence=px.colors.sequential.RdBu)),
    html.H4(children='Memory Caching (%)', style={'textAlign':'center'}),
    dcc.Graph(figure=px.pie(df[1:2], values=[df.iloc[2][1], 100 - df.iloc[2][1]], names=[df.iloc[2][0], '-'], color_discrete_sequence=px.colors.sequential.RdBu)),
])


if __name__ == '__main__':
    app.run(host='localhost', port=32168)



    

