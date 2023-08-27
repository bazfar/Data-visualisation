'''
    Provides the templates for the tooltips.
'''


def get_heatmap_hover_template():
    '''
        Sets the template for the hover tooltips in the heatmap.

        Contains three labels, followed by their corresponding
        value, separated by a colon : neighborhood, year and
        trees planted.

        The labels are font 'Roboto Slab' and bold. The values
        are font 'Roboto' and regular weight.
    '''
    
    #generate styles for heatmap
    year_title = "<span style=\"font-family:'Roboto Slab'; font-weight: bold\">Year: </span><span style=\"font-family:'Roboto'; font-weight: normal\">%{x}</span><br>"
    neighbor_title = "<span style=\"font-family:'Roboto Slab'; font-weight: bold\">Neighbourhood: </span><span style=\"font-family:'Roboto'; font-weight: normal\">%{y}</span><br>"
    tree_title = "<span style=\"font-family:'Roboto Slab'; font-weight: bold\">Trees Planted: </span><span style=\"font-family:'Roboto'; font-weight: normal\">%{z}</span><br>"

    return neighbor_title + year_title + tree_title + "<extra></extra>"

def get_linechart_hover_template():
    '''
        Sets the template for the hover tooltips in the heatmap.

        Contains two labels, followed by their corresponding
        value, separated by a colon : date and trees planted.

        The labels are font 'Roboto Slab' and bold. The values
        are font 'Roboto' and regular weight.
    '''
    #generate styles for linechart
    tree_title = "<span style=\" font-weight: bold;font-family:'Roboto Slab'\">Trees: </span><span style=\"font-weight: normal;font-family:'Roboto'\">%{y}</span><br>"
    date_title = "<span style=\" font-weight: bold;font-family:'Roboto Slab'\">Date: </span><span style=\"font-weight: normal;font-family:'Roboto';\">%{x}</span><br>"
    return date_title + tree_title + "<extra></extra>"

