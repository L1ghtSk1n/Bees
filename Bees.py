from dash import Dash, dcc, html, Input, Output
import pandas as pd
import plotly.express as px
#import plotly.graph_objects as go

df=pd.read_excel('intro_bees.xlsx')
df=df.groupby(['State', 'ANSI', 'Affected by', 'Year', 'state_code'])[['Pct of Colonies Impacted']].mean()
df.reset_index(inplace=True)
df.head()

app=Dash(__name__)

app.layout=html.Div([
    html.H1('Bees Analytics Dashboard'),
    dcc.Dropdown(id='selected_year',
                 options=[
                     {'label':'2015', 'value':2015},
                     {'label':'2016', 'value':2016},
                     {'label':'2017', 'value':2017},
                     {'label':'2018', 'value':2018}],
                 value=2015
                 ),
    html.Div(id='container',children=[]),

    dcc.Graph(id='my-graph',figure={})
])

@app.callback(
    [Output(component_id='container',component_property='children'),
    Output(component_id='my-graph',component_property='figure')],
    [Input(component_id='selected_year',component_property='value')]
)

def interactive_graph(slctd_year):

    container=f'The year chosen was {slctd_year}'

    dff = df.copy()
    dff = dff[dff["Year"] == slctd_year]
    dff = dff[dff["Affected by"] == "Varroa_mites"]

    fig = px.choropleth(
        data_frame=dff,
        locationmode='USA-states',
        locations='state_code',
        scope="usa",
        color='Pct of Colonies Impacted',
        hover_data=['State', 'Pct of Colonies Impacted'],
        color_continuous_scale=px.colors.sequential.YlOrRd,
        labels={'Pct of Colonies Impacted': '% of Bee Colonies'},
        template='plotly_dark'
    )

    # fig = go.Figure(
    #     data=[go.Choropleth(
    #         locationmode='USA-states',
    #         locations=dff['state_code'],
    #         z=dff["Pct of Colonies Impacted"].astype(float),
    #         colorscale='Reds',
    #     )]
    # )
    #
    # fig.update_layout(
    #     title_text="Bees Affected by Mites in the USA",
    #     title_xanchor="center",
    #     title_font=dict(size=24),
    #     title_x=0.5,
    #     geo=dict(scope='usa'),
    # )

    return container, fig

if __name__ == '__main__':
    app.run_server(debug=True)