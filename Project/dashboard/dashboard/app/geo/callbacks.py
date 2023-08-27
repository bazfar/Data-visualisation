from shapely.geometry import Polygon, LineString, Point
from dash.dependencies import Input, Output
import plotly.express as px  
import shapely.speedups
import plotly.io as pio
from itertools import product
import itertools
import plotly.graph_objs as go
import plotly.offline as pyo
import dash
import pandas as pd 
import geopandas as gpd
import json


### LOAD DATA ####
df_banks = pd.read_csv('app/geo/Data/geo_banks.csv')
gdf_all_banks = gpd.GeoDataFrame(df_banks, geometry=gpd.points_from_xy(df_banks.long, df_banks.lat))

def prepare_geo_data():
    geometries = gpd.read_file('app/geo/Data/TUN_adm1.shp')
    pop_pov = pd.read_csv('app/geo/Data/population_poverty.csv')
    with open('a.geojson', 'r') as file:
        geo = json.load(file)

    gov_map = {
     'Ben Arous (Tunis Sud)': 'Ben Arous',
     'Béja': 'Beja',
     'Gabès': 'Gabes',
     'Kassérine': 'Kasserine',
     'Kebili': 'Kebeli',
     'Manubah': 'Manouba',
     'Médenine': 'Mednine',
     'Sidi Bou Zid': 'Sidi Bouzid',
    }
    geometries.NAME_1 = geometries.NAME_1.apply(lambda x : gov_map[x] if x in gov_map else x)
    geometries = pd.merge(
        geometries,
        pop_pov,
        left_on='NAME_1',
        right_on='gouvernorat'
    )
    return geometries, geo


def _create_choropleth_mapbox(geometries, geo, slct_color, center, zoom):
    fig = px.choropleth_mapbox(
        geometries[['ID_1', 'NAME_1', 'geometry', slct_color]], 
        locations='ID_1', 
        geojson=geo, 
        hover_name='NAME_1', 
        color=slct_color, 
        featureidkey='properties.ID_1', 
        center=center,
        zoom=zoom,
        opacity=0.5
    )
    fig.update_geos(fitbounds="locations", visible=True, showsubunits=True, center=center)
    fig.update_layout(mapbox_style="carto-positron")
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0}) 
    return fig


def create_choropleth_mapbox(slct_color, slct_city):
    #Tunisia center
    geometries, geo = prepare_geo_data()
    center = {'lat': 33.8869, 'lon': 9.5375}
    zoom = 5
    if slct_city:
        geometries = geometries[geometries.NAME_1 == slct_city]
        zoom = 8
        centroid = geometries['geometry'].values[0].centroid
        center = {'lat': centroid.y, 'lon': centroid.x}
        fig = _create_choropleth_mapbox(geometries, geo, slct_color, center, zoom)
    else:
        fig = _create_choropleth_mapbox(geometries, geo, slct_color, center, zoom)
    return fig


def register_callbacks_geomarketing(geo):

    # Update Delegations
    @geo.callback(
        [
            dash.dependencies.Output('slct_delegat', 'options'),
            dash.dependencies.Output('slct_delegat', 'disabled')
        ],
        [dash.dependencies.Input('slct_city', 'value')])
    def set_delegations_options(slct_city):
        print('aaaaaaaaaaaaaaaaaaa')
        if slct_city is not None:
            return [[{'label': i, 'value': i} for i in gdf_all_banks[gdf_all_banks["gouvernorat"] == slct_city]['delegation'].unique()], False]
        else:
            return [[{'label': '', 'value': ''}], True]


    # Update the total number of delegations per city Tag
    @geo.callback(Output("total-delegations", "children"), [Input('slct_city', 'value')])
    def update_total_number(slct_city):
        return "Number of Delegations: {:,d}".format(
            gdf_all_banks[gdf_all_banks["gouvernorat"] == slct_city].delegation.nunique()
        )

    # Update the total number of banks branch in Tunisia
    @geo.callback(Output("total-bank-tunisia", "children"), [Input('slct_bank', 'value')])
    def update_total_number(slct_bank):
        if slct_bank:
            return "Total Number of {} Bank : {:,d}".format(slct_bank,
                                                            len(gdf_all_banks[gdf_all_banks["banque"] == slct_bank]))


    # Update the total number of banks per city Tag
    @geo.callback(Output("total-bank-city", "children"), [Input('slct_city', 'value')])
    def update_total_number(slct_city):
        return "Number of Banks within {} : {:,d}".format(slct_city,
                                                        len(
                                                            gdf_all_banks[gdf_all_banks["gouvernorat"] == slct_city])
                                                        )


    # Update the total number of banks per delegation Tag
    @geo.callback(Output("total-bank-delegation", "children"), [Input('slct_delegat', 'value')])
    def update_total_number(slct_delegat):
        return "Number of Banks within {}  : {:,d}".format(slct_delegat,
                                                        len(
                                                            gdf_all_banks[gdf_all_banks["delegation"] == slct_delegat])
                                                        )


    # Update the total number of banks branch within this city
    @geo.callback(Output("total-bank-branch-city", "children"), [Input('slct_city', 'value'), Input('slct_bank', 'value')])
    def update_total_number(slct_city, slct_bank):
        return "Number of {} Banks branch within this city {} : {:,d}".format(slct_bank.upper() if slct_bank else None, slct_city, len(gdf_all_banks[(gdf_all_banks['gouvernorat'] == slct_city) & (gdf_all_banks['banque'] == slct_bank)])
                                                                            )


    # Update the total number of banks branch within this delegations
    @geo.callback(Output("total-bank-branch-delegation", "children"), [Input('slct_delegat', 'value'), Input('slct_bank', 'value')])
    def update_total_number(slct_delegat, slct_bank):
        return "Number of {} Banks branch within this delegation : {:,d}".format(slct_bank.upper() if slct_bank else None,
                                                                                len(gdf_all_banks[(gdf_all_banks['delegation'] == slct_delegat) & (
                                                                                    gdf_all_banks['banque'] == slct_bank)])
                                                                                )


    # Linking Graph and inputs
    @geo.callback(
        Output(component_id='my_bee_map', component_property='figure'),
        [Input(component_id='slct_city', component_property='value'),
        Input(component_id='slct_delegat', component_property='value'),
        Input(component_id='slct_bank', component_property='value'),
        Input(component_id='slct_color', component_property='value'),
        ]
    )
    def update_graph(slct_city, slct_delegat, slct_bank, slct_color):

        print(slct_city, slct_delegat, slct_bank, slct_color)

        fig2 = create_choropleth_mapbox(slct_color, slct_city)

        # if city is selected only
        if (slct_city and not slct_delegat and not slct_bank):
            
            dff = gdf_all_banks.copy()
            dff = dff[dff["gouvernorat"] == slct_city]
            fig = px.scatter_mapbox(dff, lat="lat", lon="long",
                                    hover_name="banque", hover_data=["gouvernorat", "delegation"], zoom=8)
            fig.update_layout(mapbox_style="carto-positron")
            fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
            fig.update_traces(marker={'size': 8})
            # #add scatter 
            for i in range(len(fig.data)):
                fig2.add_trace(fig.data[i])
            fig2.update_layout(showlegend=False)
            return fig2

        # if city & delegation selected
        if (slct_city and slct_delegat and not slct_bank):

            dff = gdf_all_banks.copy()
            dff = dff[dff["gouvernorat"] == slct_city]
            dff = dff[dff["delegation"] == slct_delegat]
            fig = px.scatter_mapbox(dff, lat="lat", lon="long",
                                    hover_name="banque",hover_data=["gouvernorat", "delegation"], zoom=10)
            fig.update_layout(mapbox_style="carto-positron")
            fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
            fig.update_traces(marker={'size': 10})

            # #add scatter 
            for i in range(len(fig.data)):
                fig2.add_trace(fig.data[i])
            fig2.update_layout(showlegend=False)
            return fig2

        # if bank is selected only
        if ( not slct_city and not slct_delegat and slct_bank):
            print(slct_bank,slct_city,slct_delegat)
            dff = gdf_all_banks.copy()
            dff = dff[dff["banque"] == slct_bank]
            fig = px.scatter_mapbox(dff, lat="lat", lon="long",
                                    hover_name="gouvernorat",hover_data=["gouvernorat", "delegation"], zoom=7.5)
            fig.update_layout(mapbox_style="carto-positron")
            fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
            fig.update_traces(marker={'size': 10})

            # #add scatter 
            for i in range(len(fig.data)):
                fig2.add_trace(fig.data[i])
            fig2.update_layout(showlegend=False)
            return fig2

        # if city & bank selected

        if (slct_city and slct_bank and not slct_delegat):

            dff = gdf_all_banks.copy()
            # print(dff[(dff['banque']=="amen")].gouvernorat.unique())
            dff = dff[(dff["gouvernorat"] == slct_city)
                    & (dff["banque"] == slct_bank)]
           
            fig = px.scatter_mapbox(dff, lat="lat", lon="long", color='banque',
                                    hover_name="banque",hover_data=["gouvernorat", "delegation"], zoom=10)
            fig.update_layout(mapbox_style="carto-positron")
            fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
            fig.update_traces(marker={'size': 10})

            # #add scatter 
            for i in range(len(fig.data)):
                fig2.add_trace(fig.data[i])
            fig2.update_layout(showlegend=False)
            return fig2

        # if city & delegation & bank selected
        if (slct_city and slct_delegat and slct_bank ):

            dff = gdf_all_banks.copy()
            dff = dff[dff["gouvernorat"] == slct_city]
            dff = dff[dff["delegation"] == slct_delegat]
            dff = dff[dff["banque"] == slct_bank]
            fig = px.scatter_mapbox(dff, lat="lat", lon="long",
                                    hover_name="banque",hover_data=["gouvernorat", "delegation"], zoom=10)
            fig.update_layout(mapbox_style="carto-positron")
            fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
            fig.update_traces(marker={'size': 10})

            # #add scatter 
            for i in range(len(fig.data)):
                fig2.add_trace(fig.data[i])
            fig2.update_layout(showlegend=False)
            return fig2

        #nothing is selected / initial state
        else:
            dff = gdf_all_banks.copy()
            fig = px.scatter_mapbox(gdf_all_banks, lat="lat", lon="long",
                                    hover_name="banque",hover_data=["gouvernorat", "delegation"], zoom=5)
            fig.update_layout(mapbox_style="carto-positron")
            fig.update_layout(margin={"r": 0, "t": 0, "l": 150, "b": 0})
            fig.update_traces(marker={'size': 10})
            fig.update_traces(marker={'size': 10})
            # #add scatter 
            for i in range(len(fig.data)):
                fig2.add_trace(fig.data[i])
            fig2.update_layout(showlegend=False)
            return fig2


    @geo.callback(
        Output(component_id='second_graph', component_property='figure'),
        [Input(component_id='slct_city', component_property='value'),
        Input(component_id='slct_delegat', component_property='value'),
        Input(component_id='slct_bank', component_property='value')]
    )
    def update_graph(slct_city, slct_delegat, slct_bank):

        # if city & delegation selected
        if (slct_city and slct_delegat):
        
            bank_data = gdf_all_banks[gdf_all_banks["delegation"] == slct_delegat]
            fig = px.bar(
                data_frame=bank_data,
                x=bank_data['banque'].value_counts().keys(),
                y=bank_data['banque'].value_counts().values,
                title="Number of Banks Within this delegation {}".format(
                    slct_delegat),
                labels=dict(x="banks"))
            fig.update_traces(marker_color='rgb(158,202,225)', marker_line_color='rgb(8,48,107)',
                    marker_line_width=1.5, opacity=0.6)
            fig.update_layout(margin=dict(l=150))
            fig.update_yaxes(title='')
            fig.add_annotation(x=-0.12, y=bank_data['banque'].value_counts().values.max()/2, xref="paper", yref="y", showarrow=False, text="Number <br> of <br> branches", font=dict(size=14), textangle=0)

            
            return fig

        # city selected
        if (slct_city  and not slct_delegat and not slct_bank):
        
            bank_data = gdf_all_banks[gdf_all_banks["gouvernorat"] == slct_city]
            fig = px.bar(
                data_frame=bank_data,
                x=bank_data['banque'].value_counts().keys(),
                y=bank_data['banque'].value_counts().values,
                title="Number of Banks Within this city {}".format(slct_city),
                labels=dict(x="Banks", y="Number of branches "))
            fig.update_traces(marker_color='rgb(158,202,225)', marker_line_color='rgb(8,48,107)',
                    marker_line_width=1.5, opacity=0.6)
            fig.update_layout(margin=dict(l=150))
            fig.update_yaxes(title='')
            fig.add_annotation(x=-0.12, y=bank_data['banque'].value_counts().values.max()/2, xref="paper", yref="y", showarrow=False, text="Number <br> of <br> branches", font=dict(size=14), textangle=0)

            return fig

        else:
        

            fig = px.bar(
                data_frame=gdf_all_banks,
                x=gdf_all_banks['banque'].value_counts().keys(),
                y=gdf_all_banks['banque'].value_counts().values,
                title="Overall Number of bank branches inside Tunisia",
                labels=dict(x="Banks", y="Number of branches "))
            fig.update_traces(marker_color='rgb(158,202,225)', marker_line_color='rgb(8,48,107)',
                    marker_line_width=1.5, opacity=0.6)
            fig.update_yaxes(title='')
            fig.update_layout(margin=dict(l=150))
            fig.add_annotation(x=-0.12, y=gdf_all_banks['banque'].value_counts().values.max()/2, xref="paper", yref="y", showarrow=False, text="Number <br> of <br> branches", font=dict(size=14), textangle=0)

            return fig
