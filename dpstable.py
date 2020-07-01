import table
import format


class DPSTable(table.Table):
    def __init__(self, event_data, player_data):
        super(DPSTable, self).__init__(event_data, player_data)

    def get_totals(self, eq_class):
        if not self.is_class_included(eq_class):
            return []

        return list(self.total)

    def _format_row_data(self, num):
        return format.humanize(num)

    def _get_drop_columns(self):
        return ['pct', 'dps', 'time']
