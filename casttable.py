import pandas as pd
import table


class CastTable(table.Table):
    def __init__(self, event_data, player_data, blocklist):
        self.blocklist = blocklist
        super(CastTable, self).__init__(event_data, player_data)

    def get_totals(self, eq_class):
        if not self.is_class_included(eq_class):
            return []

        t = self._get_table(eq_class)
        totals = t.sum()
        return list(totals)

    def _get_table(self, eq_class=None):
        t = super(CastTable, self)._get_table(eq_class)\
            .dropna(axis='columns', how='all')\
            .fillna(0)\
            .set_index('alias')\
            .T\
            .astype('int32')

        t = t.reindex(sorted(t.index), axis='rows')
        return t

    def _get_drop_columns(self):
        return self.blocklist


def aggregate(cast_data_list):
    t = cast_data_list[0]

    if len(cast_data_list) > 1:
        cast_tables = list()
        for cd in cast_data_list:
            cast_tables.append(cd.data)
        t.data = pd.concat(cast_tables).groupby(level=0).max()

    return t

