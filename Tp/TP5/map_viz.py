'''
    Contains the functions to set up the map visualization.

'''

import plotly.graph_objects as go
import plotly.express as px

import hover_template as hover


def add_choro_trace(fig, montreal_data, locations, z_vals, colorscale):
    '''
        Adds the choropleth trace, representing Montreal's neighborhoods.

        Note: The z values and colorscale provided ensure every neighborhood
        will be grey in color. Although the trace is defined using Plotly's
        choropleth features, we are simply defining our base map.

        The opacity of the map background color should be 0.2.

        Args:
            fig: The figure to add the choropleth trace to
            montreal_data: The data used for the trace
            locations: The locations (neighborhoods) to show on the trace
            z_vals: The table to use for the choropleth's z values
            colorscale: The table to use for the choropleth's color scale
        Returns:
            fig: The updated figure with the choropleth trace

    '''
    fig_trace = px.choropleth_mapbox(locations=locations,
                                 color=z_vals,
                                 color_continuous_scale=colorscale,
                                 mapbox_style='carto-positron',
                                 color_discrete_map={1: colorscale[0]},
                                 geojson=montreal_data,
                                 featureidkey='properties.NOM',
                                 opacity=0.2
                                 )
    
    #add hover and legend
    fig_trace.update_traces(
                        hovertemplate=hover.map_base_hover_template(),
                        showlegend=False
                        )
    
    fig.add_trace(fig_trace.data[0])
    fig.update_layout(autosize=True,
                      coloraxis= dict(colorscale='Greys'),
                      coloraxis_showscale=False
                      )
    return fig


def add_scatter_traces(fig, street_df):
    '''
        Adds the scatter trace, representing Montreal's pedestrian paths.

        The marker size should be 20.

        Args:
            fig: The figure to add the scatter trace to
            street_df: The dataframe containing the information on the
                pedestrian paths to display
        Returns:
            The figure now containing the scatter trace

    '''
    street_df['lon'] = street_df['geometry.coordinates'].apply(lambda x: x[0])
    street_df['lat'] = street_df['geometry.coordinates'].apply(lambda x: x[1])
    name = street_df["properties.TYPE_SITE_INTERVENTION"]

    fig_trace = px.scatter_mapbox(street_df, 
                                  lon='lon', 
                                  lat='lat',
                                  color="properties.TYPE_SITE_INTERVENTION",
                                  color_discrete_map={},
                                  zoom=10,
                                  custom_data = street_df
                              )
    #add marker size and hover
    fig_trace.update_traces(marker=dict(size=20),
                        hovertemplate=name.apply(hover.map_marker_hover_template))

    for trace in fig_trace.data:
        fig.add_trace(trace)
    fig.update_traces()
    
    #legend and hovermdoe
    fig.update_layout(autosize=True,
                      legend=dict(bgcolor='rgba(0, 0, 0, 0)', 
                                  itemsizing='constant'
                                  ),
                      hovermode='closest'
                      )
    return fig
