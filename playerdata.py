import pandas as pd


class PlayerData:
    """
    PlayerData tracks the name, class, and alias of a list of players.
    """

    def __init__(self, path):
        """
        Read a player config file into a pandas data frame with columns name, class, alias.

        The config file should be in CSV format with the values name, class, alias.

        :param path: path to the config CSV file
        :return: A data frame with columns name, class, alias
        """
        headers = ['name', 'class', 'alias']
        stripping_sep = ' *, *'
        data = pd.read_csv(path, names=headers, sep=stripping_sep, engine='python')

        # clean up - remove NaN and duplicate rows, set NaN aliases to name, all other NaNs to UNKNOWN
        data.drop_duplicates(inplace=True)
        data.dropna(how='all', inplace=True)
        data.loc[data['alias'].isnull(), 'alias'] = data.loc[data['alias'].isnull(), 'name']
        data.fillna('UNKNOWN', inplace=True)

        self.data = data

    def is_player(self, player):
        return player in self.data['name'].unique()

    def get_data(self):
        """
        Retrieves the data frame managed by a PlayerData object.

        :return: a data frame containing the name, class, and alias of all players read in from file
        """
        return self.data

    def _get_player_attribute(self, player, attribute):
        if not self.is_player(player):
            return 'unknown'

        player_idx = self.data.index[self.data['name'] == player].values[0]
        return self.data.at[player_idx, attribute]

    def get_player_class(self, player):
        return self._get_player_attribute(player, 'class')

    def get_player_alias(self, player):
        return self._get_player_attribute(player, 'alias')
