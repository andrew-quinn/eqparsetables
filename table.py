import pandas as pd


class Table:
    def __init__(self, event_data, player_data):
        self.data = self._sanitize_table(pd.DataFrame(event_data), player_data)

    def get_classes(self):
        return self.data['class'].dropna().unique()

    def is_class_included(self, eq_class):
        if eq_class is None:
            return True

        return eq_class in self.get_classes()

    def get_players(self):
        return list(self.data['alias'])

    def get_rows(self, eq_class=None):
        if not self.is_class_included(eq_class):
            return []

        table = self._get_table(eq_class)
        row_names = list(table.index)

        counts = []
        for s in row_names:
            counts.append([s] + [self._format_row_data(n) for n in list(table.loc[s])])
        return [''] + table.columns.tolist(), counts

    def _format_row_data(self, num):
        return str(num)

    def _get_table(self, eq_class=None):
        if eq_class is None:
            table = self.data
        else:
            table = self.data.loc[self.data['class'] == eq_class]

        table = table.drop(['class', 'name'], axis='columns')
        cols = table.columns.tolist()
        cols.remove('alias')
        cols.insert(0, 'alias')
        table = table[cols]

        return table

    def _get_drop_columns(self):
        return []

    def _is_drop_column(self, col):
        drop_cols = self._get_drop_columns()
        for prefix in drop_cols:
            if col.startswith(prefix):
                return True
        return False

    def _sanitize_table(self, df, player_data):
        df = pd.merge(df, player_data.get_data(), how='left')
        drop_cols = [col for col in df.columns if self._is_drop_column(col)]

        df.drop(df[drop_cols], axis='columns', inplace=True)
        return df
