'''
    Contains some functions to preprocess the data used in the visualisation.
'''
import pandas as pd

TITLES = {
    # pylint: disable=line-too-long
    '1. Noyau villageois': 'Noyau villageois',
    '2. Rue commerciale de quartier, d’ambiance ou de destination': 'Rue commerciale de quartier, d’ambiance ou de destination', # noqa : E501
    '3. Rue transversale à une rue commerciale': 'Rue transversale à une rue commerciale', # noqa : E501
    '4. Rue bordant un bâtiment public ou institutionnel  (tels qu’une école primaire ou secondaire, un cégep ou une université, une station de métro, un musée, théâtre, marché public, une église, etc.)': 'Rue bordant un bâtiment public ou institutionnel', # noqa : E501
    '5. Rue en bordure ou entre deux parcs ou place publique': 'Rue en bordure ou entre deux parcs ou place publique', # noqa : E501
    '6. Rue entre un parc et un bâtiment public ou institutionnel': 'Rue entre un parc et un bâtiment public ou institutionnel', # noqa : E501
    '7. Passage entre rues résidentielles': 'Passage entre rues résidentielles'
}


def to_df(data):
    '''
        Converts the data to a pandas dataframe.

        Args:
            data: The data to convert
        Returns:
            my_df: The corresponding dataframe
    '''
    my_df = pd.json_normalize(data, record_path="features")
    return my_df


def update_titles(my_df):
    '''
        Updates the column "TYPE_SITE_INTERVENTION" with corresponding
        values from the 'TITLES' dictionary (above).

        Args:
            my_df: The dataframe to update
        Returns:
            my_df: The dataframe with the appropriate replacements
                made according to the 'TITLES' dictionary
    '''
    my_df['properties.TYPE_SITE_INTERVENTION'] = my_df['properties.TYPE_SITE_INTERVENTION'].map(TITLES)
    return my_df


def sort_df(my_df):
    '''
        Sorts the dataframe by the column "TYPE_SITE_INTERVENTION" in
        alphabetical order.

        Args:
            my_df: The dataframe to sort
        Returns:
            my_df: The sorted dataframe
    '''
    
    #sort dataframe by TYPE_SITE_INTERVENTION
    my_df.sort_values(by=["properties.TYPE_SITE_INTERVENTION"], ascending=True, inplace=True)
    return my_df


def get_neighborhoods(montreal_data):
    '''
        Gets the name of the neighborhoods in the dataset

        Args:
            montreal_data: The data to parse
        Returns:
            locations: An array containing the names of the
                neighborhoods in the data set
    '''
    #get names of neighborhoods
    montreal_df = to_df(montreal_data)
    locations = montreal_df['properties.NOM'].to_numpy()
    return locations
