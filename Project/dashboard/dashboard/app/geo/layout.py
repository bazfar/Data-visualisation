
import dash_core_components as dcc
import dash_html_components as html
import warnings
warnings.filterwarnings("ignore")
import time
# Import the necessaries libraries
import pandas as pd 
import geopandas as gpd 


df_banks = pd.read_csv('app/geo/Data/geo_banks.csv')
gdf_all_banks = gpd.GeoDataFrame(df_banks, geometry=gpd.points_from_xy(df_banks.long, df_banks.lat))

geo_page = html.Div(
    children=[
        html.Div(
            className="row",
            children=[
                # Column for user controls
                html.Div(
                    className="four columns div-user-controls",
                    children=[
                        # # html.A(
                        # #     html.Img(
                        # #         className="logo",
                        # #         src=("assets\download.png"),
                                
                        # #     ),
                        # #     href="#",
                        # ),
                        html.H2("BANKING GEOMARKETING TOOL"),
                        html.Div(
                            className="div-for-dropdown",
                            children=[
                                # Dropdown to select Bank
                                dcc.Dropdown(
                                    id="slct_color", options=[{"label": 'Population', "value": '2021'}, {"label": 'Poverty Rate', "value": 'poverty_rate'}], multi=False,
                                    placeholder="Select color",
                                    clearable=False,
                                    value='poverty_rate'
                                )
                            ],
                        ),
                        html.P(
                            """Select different cities ,delegation and banks using the dropdown item."""
                        ),
                        html.Div(
                            className="div-for-dropdown",
                            children=[
                                dcc.Dropdown(id="slct_city",
                                             options=[{"label": i, "value": i} for i in gdf_all_banks['gouvernorat'].unique()
                                                      ], multi=False, style={"border": "0px solid black"},
                                             placeholder="Select a state")
                            ],
                        ),
                        # Change to side-by-side
                        html.Div(
                            className="row",
                            children=[
                                html.Div(
                                    className="div-for-dropdown",
                                    children=[
                                        # Dropdown for locations on map
                                        dcc.Dropdown(
                                            id="slct_delegat", options=[{"label": i, "value": i}
                                                                        for i in gdf_all_banks['delegation'].unique()], multi=False,
                                            placeholder="Select a delegation",
                                            disabled=True
                                        )
                                    ],
                                ),
                                html.Div(
                                    className="div-for-dropdown",
                                    children=[
                                        # Dropdown to select Bank
                                        dcc.Dropdown(
                                            id="slct_bank", options=[{"label": i, "value": i}
                                                                     for i in gdf_all_banks['banque'].unique()], multi=False,
                                            placeholder="Select bank",
                                        )
                                    ],
                                ),
                            ],
                        ),
                        html.P(id="total-delegations"),
                        html.P(id="total-bank-tunisia"),
                        html.P(id="total-bank-city"),
                        html.P(id="total-bank-branch-city"),
                        html.P(id="total-bank-delegation"),
                        html.P(id="total-bank-branch-delegation"),
                        dcc.Markdown(
                            """
                            **Created by Group 9**
                    
                            """
                        ),
                    ],
                ),


                # Column for app graphs and plots
                html.Div(
                    className="eight columns div-for-charts bg-grey",
                    children=[
                        dcc.Graph(id="my_bee_map"),
                        dcc.Graph(id="second_graph"),

                    ],
                )

            ],
        )
    ]
)