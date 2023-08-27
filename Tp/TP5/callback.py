'''
    This file contains the functions to call when
    a click is detected on the map, depending on the context
'''
import dash_html_components as html


def no_clicks(style):
    '''
        Deals with the case where the map was not clicked

        Args:
            style: The current display style for the panel
        Returns:
            title: The updated display title
            mode: The updated display title
            theme: The updated display theme
            style: The updated display style for the panel
    '''
    style['visibility'] = 'hidden'
    return None, None, None, style


def map_base_clicked(title, mode, theme, style):
    '''
        Deals with the case where the map base is
        clicked (but not a marker)

        Args:
            title: The current display title
            mode: The current display title
            theme: The current display theme
            style: The current display style for the panel
        Returns:
            title: The updated display title
            mode: The updated display title
            theme: The updated display theme
            style: The updated display style for the panel
    '''
    return title, mode, theme, style


def map_marker_clicked(figure, curve, point, title, mode, theme, style): # noqa : E501 pylint: disable=unused-argument too-many-arguments line-too-long
    '''
        Deals with the case where a marker is clicked

        Args:
            figure: The current figure
            curve: The index of the curve containing the clicked marker
            point: The index of the clicked marker
            title: The current display title
            mode: The current display title
            theme: The current display theme
            style: The current display style for the panel
        Returns:
            title: The updated display title
            mode: The updated display title
            theme: The updated display theme
            style: The updated display style for the panel
    '''
    info_marker = figure['data'][curve]['customdata'][point]
    name = info_marker[4]   
    mode = info_marker[16]  
    theme = info_marker[23] 
    

    # Update the panel 
    title = html.Div(html.H3(name), id='marker-title', 
                     style={'color': figure['data'][curve]['marker']['color'],
                            'padding': '0',
                            'marginTop': '-30px'
                            }
                     )  
    mode = html.Div(html.P(f"{mode}"), 
                    id='mode', 
                    style={'padding': '0','marginTop': '-20px'}
                    )  

    # Create a list of themes
    if theme is not None:
        theme_list = [html.Li(theme_item) for theme_item in theme.split('\n')]
        thematique = 'Thématique:'
    else:
        theme_list = []
        thematique = 'Thématique: Aucune' 
        
    theme = html.Div([html.P(thematique, ),html.Ul(theme_list)], 
                     id='theme',
                     style={'padding': '0','marginTop': '-20px'}
                     ) 
 
    # new panel
    style['height'] = 'min-content'
    style['visibility'] = 'visible'
    style['display'] = 'block'
    style['background-color'] = 'transparent'

    
    return title, mode, theme, style
