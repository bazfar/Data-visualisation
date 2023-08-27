'''
    Contains some functions to preprocess the data used in the visualisation.
'''
import pandas as pd
from modes import MODE_TO_COLUMN


def summarize_lines(my_df):
    '''
        Sums each player's total of number of lines and  its
        corresponding percentage per act.

        The sum of lines per player per act is in a new
        column named 'PlayerLine'.

        The percentage of lines per player per act is
        in a new column named 'PlayerPercent'

        Args:
            my_df: The pandas dataframe containing the data from the .csv file
        Returns:
            The modified pandas dataframe containing the
            information described above.
    '''
    # TODO : Modify the dataframe, removing the line content and replacing
    # it by line count and percent per player per act
    #return my_df

    player_lines = my_df.groupby(['Player', 'Act'])['Line'].count().reset_index()
    player_lines = player_lines.rename(columns={'Line': 'LineCount'})

    act_lines = my_df.groupby('Act')['Line'].count().reset_index()
    act_lines = act_lines.rename(columns={'Line': 'ActLine'})

    merged_df = pd.merge(player_lines, act_lines, on='Act')

    merged_df['LinePercent'] = merged_df['LineCount'] / merged_df['ActLine'] * 100
    merged_df = merged_df.drop('ActLine', axis=1)
    
    return merged_df

def replace_others(my_df):
    '''
        For each act, keeps the 5 players with the most lines
        throughout the play and groups the other plyaers
        together in a new line where :

        - The 'Act' column contains the act
        - The 'Player' column contains the value 'OTHER'
        - The 'LineCount' column contains the sum
            of the counts of lines in that act of
            all players who are not in the top
            5 players who have the most lines in
            the play
        - The 'PercentCount' column contains the sum
            of the percentages of lines in that
            act of all the players who are not in the
            top 5 players who have the most lines in
            the play

        Returns:
            The df with all players not in the top
            5 for the play grouped as 'OTHER'
    '''
    #TODO : Replace players in each act not in the top 5 by a
    # new player 'OTHER' which sums their line count and percentage    
        
    modified_df = pd.DataFrame(columns=my_df.columns)  

    top_player_names = my_df.groupby('Player')['LineCount'].sum().nlargest(5)    
    top_players = my_df[my_df['Player'].isin(top_player_names.index)]

    for act in my_df['Act'].unique():

        act_df = my_df[my_df['Act'] == act]


        other_line_count = act_df.loc[~act_df['Player'].isin(top_players['Player']), 'LineCount'].sum()
        other_line_percent = act_df.loc[~act_df['Player'].isin(top_players['Player']), 'LinePercent'].sum()
        top_player_act = act_df.loc[act_df['Player'].isin(top_players['Player'])]

        others_row = pd.DataFrame({
            'Player': ['Others'],
            'Act': [act],
            'LineCount': [other_line_count],
            'LinePercent': [other_line_percent]
        })
        
        modified_act_df = pd.concat([top_player_act, others_row], axis=0)
        modified_df = pd.concat([modified_df, modified_act_df], axis=0)
        
    modified_df = modified_df[['Act', 'Player', 'LineCount','LinePercent']]
    modified_df.reset_index(drop=True, inplace=True) 
    return modified_df


def clean_names(my_df):
    '''
        In the dataframe, formats the players'
        names so each word start with a capital letter.

        Returns:
            The df with formatted names
    '''
    # TODO : Clean the player names
    my_df['Player'] = my_df['Player'].str.capitalize()
    return my_df
