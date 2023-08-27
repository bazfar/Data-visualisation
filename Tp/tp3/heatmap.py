'''
    Contains some functions related to the creation of the heatmap.
'''
import plotly.express as px
import hover_template


def get_figure(data):
    '''
        Generates the heatmap from the given dataset.

        Make sure to set the title of the color bar to 'Trees'
        and to display each year as an x-tick. The x and y axes should
        be titled "Year" and "Neighborhood". 

        Args:
            data: The data to display
        Returns:
            The figure to be displayed.
    '''
    #draw heatmap
    heat_label = {
        "color": "Trees",
        "x": "Year",
        "y": "Neighborhood",
    }
    heat_fig = px.imshow(data, labels=heat_label)
    heat_fig.update_traces(hovertemplate=hover_template.get_heatmap_hover_template())
    heat_fig.update_xaxes(dtick=1)
    heat_fig.update_layout(dragmode=False)
    return heat_fig
    