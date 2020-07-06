import operator as op
import os

import pygal as pg
import pygal.style as style

import everquestinfo as eq


class SpellFilter:
    """
    A simple container class used to classify spells.
    """

    def __init__(self, name, spells):
        """
        Construct a SpellFilter object.

        :param name: the name of the spell type, e.g. "Heals"
        :param spells: a list of spells of type 'name'
        """
        self.name = name
        self.spells = spells


def graph_heals(players, rows, eq_class, separate_spells=False):
    """
    Gather up heal spells and create healing graphs for each priest class.

    :param players: the players for whom data has been collected
    :param rows: the name of each spell and the number of casts per player
    :param eq_class: the class of players to be graphed (e.g., CLR)
    :param separate_spells: flag specifying whether heals should be grouped by type or named individually
    :return: void
    """
    heal_filter = SpellFilter('Heals', eq.heals)
    graph_spells(players, rows, eq_class, heal_filter, separate_spells)

    return


def graph_utilities(players, rows, eq_class, separate_spells=False):
    """
    Gather up utility spells and create healing graphs for each priest class.

    :param players: the players for whom data has been collected
    :param rows: the name of each spell and the number of casts per player
    :param eq_class: the class of players to be graphed (e.g., CLR)
    :param separate_spells: flag specifying whether utility spells should be grouped by type or named individually
    :return: void
    """
    utility_filter = SpellFilter('Utility', eq.utilities)
    graph_spells(players, rows, eq_class, utility_filter, separate_spells)

    return


def graph_nukes(players, rows, eq_class, separate_spells=False):
    """
    Gather up direct damage spells and create healing graphs for each priest class.

    :param players: the players for whom data has been collected
    :param rows: the name of each spell and the number of casts per player
    :param eq_class: the class of players to be graphed (e.g., CLR)
    :param separate_spells: flag specifying whether nukes should be grouped by type or named individually
    :return: void
    """
    nuke_filter = SpellFilter('Nukes', eq.nukes)
    graph_spells(players, rows, eq_class, nuke_filter, separate_spells)

    return


def get_unpopulated_chart(title, players):
    """
    Create a chart with a title and labeled axes.

    :param title: the chart title
    :param players: a list of players to appear on the x-axis
    """
    st = style.DarkStyle
    st.font_family = "DeJa Vu Sans"
    st.value_font_size = 8
    chart = pg.StackedBar(style=st, print_values=True, print_zeroes=False)
    chart.show_minor_y_labels = True
    chart.title = title
    chart.x_labels = players
    chart.value_formatter = lambda x: '{0:d}'.format(int(x))
    return chart


def graph_spells(players, rows, eq_class, spell_filter, separate_spells=False):
    """
    Create bar graphs associating cast counts and spells to their respective casters.

    :param players: the players for whom data has been collected
    :param rows: the name of each spell and the number of casts per player
    :param eq_class: the class of players to be graphed (e.g., CLR)
    :param spell_filter: a typical grouping of spells into heals, utility, or nukes
    :param separate_spells: a flag indicating whether spells should be grouped by type or named individually
    :return: void
    """
    class_name = eq.get_class_name(eq_class)
    title = '{0}: {1}'.format(class_name, spell_filter.name)
    chart = get_unpopulated_chart(title, players[1:])

    if separate_spells:
        spells = [row for row in rows if row[0] in spell_filter.spells.keys()]
        for spell in spells:
            chart.add(spell[0], spell[1:])
    else:
        spell_types = dict()
        for row in rows:
            t = spell_filter.spells.get(row[0], '')
            if t:
                vs = [int(v) for v in row[1:]]
                spell_types[t] = map(op.add, spell_types.get(t, [0] * len(vs)), vs)
        for spell_type in sorted(spell_types.keys()):
            chart.add(spell_type, list(spell_types[spell_type]))

    chart.render_to_png('{0}/{1}_{2}.png'.format(os.getcwd(), class_name.lower(), spell_filter.name.lower()))


def generate_class_graphs(players, rows, eq_class):
    """
    Create spell cast graphs for each supported EQ class.

    :param players: the players for whom data has been collected
    :param rows: the name of each spell and the number of casts per player
    :param eq_class: the class of players to be graphed (e.g., CLR)
    :return: void
    """
    dispatch = {
        'CLR': [graph_heals, graph_utilities, graph_nukes],
        'DRU': [graph_heals, graph_utilities, graph_nukes],
        'SHM': [graph_heals, graph_utilities, graph_nukes]
    }

    for f in dispatch.get(eq_class, []):
        f(players, rows, eq_class)


def graph_dps(rows, eq_class=None):
    if eq_class is None:
        class_name = 'All'
    else:
        class_name = eq.get_class_name(eq_class)

    title = 'SDPS: {0}'.format(class_name)

    st = style.DarkStyle
    st.font_family = "DeJa Vu Sans"
    # st.label_font_size = 12
    chart = pg.HorizontalBar(
        style=st,
        title=title,
        show_legend=False,
        print_labels=True,
        )

    for row in rows:
        chart.add(row[0], [{'value': row[1], 'label': '{0}: {1}'.format(row[0], row[1])}])

    chart.render_to_png('{0}/sdps_{1}.png'.format(os.getcwd(), class_name.lower()))
