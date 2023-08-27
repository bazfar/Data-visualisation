'''
    Provides the templates for the tooltips.
'''


def map_base_hover_template():
    '''
        Sets the template for the hover tooltips on the neighborhoods.

        The label is simply the name of the neighborhood in font 'Oswald'.

        Returns:
            The hover template.
    '''
    #create neighborhood template style
    neighbor_template = "<b><span style='font-family: Oswald'>%{properties.NOM}</span></b>"
    return neighbor_template



def map_marker_hover_template(name):
    '''
        Sets the template for the hover tooltips on the markers.

        The label is simply the name of the walking path in font 'Oswald'.

        Args:
            name: The name to display
        Returns:
            The hover template.
    '''
    #create marker template style
    marker_template = "<b><span style='font-family: Oswald'>%{fullData.name}</span></b> <extra></extra>"
    return marker_template