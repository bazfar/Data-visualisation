'''
    Contains some functions related to the creation of the line chart.
'''
import plotly.express as px
import plotly.graph_objects as go
import hover_template

from template import THEME


def get_empty_figure():
    '''
        Returns the figure to display when there is no data to show.

        The text to display is : 'No data to display. Select a cell
        in the heatmap for more information.

    '''
    
    #create empty figure with specified text
    empty_scatter = go.Scatter(x=[], y=[])
    display_text = {
        'x': 0.5,
        'y': 0.5,
        'showarrow': False,
        'font': {'size': 12} ,
        'text': 'No data to display. Select a cell in the heatmap for more information.',
    }
    
    empty_layout = {
        'ticks': '',
        'showticklabels': False,
        'showgrid': False,
        'zeroline': False,
        'showline': False
    }

    empty_layout = go.Layout(
        dragmode=False,
        showlegend=False,
        annotations=[display_text],
        xaxis=empty_layout,
        yaxis=empty_layout,
    )

    fig = go.Figure(data=[empty_scatter], layout=empty_layout)
    return fig


def add_rectangle_shape(fig):
    '''
        Adds a rectangle to the figure displayed
        behind the informational text. The color
        is the 'pale_color' in the THEME dictionary.

        The rectangle's width takes up the entire
        paper of the figure. The height goes from
        0.25% to 0.75% the height of the figure.
    '''
    
    #create the rectangle
    fig.update_yaxes(range=[0, 1])
    fig.update_xaxes(range=[0, 1])

    fig.add_shape(
        type='rect',
        layer='below',
        fillcolor=THEME['pale_color'],
        line_color=THEME['pale_color'],
        x0=0,
        x1=1,
        y0=0.25,
        y1=0.75
    )

    return fig



def get_figure(line_data, arrond, year):
    '''
        Generates the line chart using the given data.

        The ticks must show the zero-padded day and
        abbreviated month. The y-axis title should be 'Trees'
        and the title should indicated the displayed
        neighborhood and year.

        In the case that there is only one data point,
        the trace should be displayed as a single
        point instead of a line.

        Args:
            line_data: The data to display in the
            line chart
            arrond: The selected neighborhood
            year: The selected year
        Returns:
            The figure to be displayed
    '''
    #get line chart mode
    line_mode = ''
    if(len(line_data) == 1):
     line_mode = 'markers' 
    else:
     line_mode = 'lines'   
      
    line_trace = go.Scatter(
        mode=line_mode,
        x=line_data['Date_Plantation'],
        y=line_data['Counts'],
    )
    
    line_fig = go.Figure(
        layout_title_text=f'Trees planted in {arrond} in {year}',
        data=[line_trace]
    )
    
    #draw line chart
    line_fig.update_traces(hovertemplate=hover_template.get_linechart_hover_template())
    line_fig.update_xaxes(tickformat='%d %b', tickangle=-45)
    line_fig.update_yaxes(title_text='Trees')
    
    return line_fig