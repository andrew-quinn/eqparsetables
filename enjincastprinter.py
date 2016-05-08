import parsedb


def print_cast_table(table: parsedb.CastTable):
    print('[size=5][b]{0}[/b][/size]'.format(table.class_name))
    print('[table]')
    print('[tr][td][/td][td][b]{0}[/b][/td][/tr]'
          .format('[/b][/td][td][b]'.join(str(cell) for cell in table.get_players())))
    print('[tr][td][b]Total[/b][/td][td][b]{0}[/b][/td][/tr]'
          .format('[/b][/td][td][b]'.join(str(cell) for cell in table.get_totals())))
    spells = table.get_spells()
    for i, row in enumerate(table.get_rows()):
        print('[tr][td]{0}[/td][td]{1}[/td][/tr]'.format(spells[i], '[/td][td]'.join(str(cell) for cell in row)))
    print('[/table]')


def print_cast_tables(tables: [parsedb.CastTable]):
    """
    Print all parsed class tables in enjin forum table format.

    :param tables: list of CastTables to be printed
    :return: void
    """
    for loop_count, table in enumerate(tables):
        padding = '\n\n' if loop_count else ''
        print(padding)
        print_cast_table(table)


def print_dps_table(mob, fight_time, guild_stats, dpser_dod):
    print('[size=5][b]{0} in {1} seconds[/b][/size]'.format(mob, fight_time))
    print('[table]')
    print('[tr][td][b][/b][/td][td][b]SDPS[/b][/td][td][b]Total DMG[/b][/td][td][b]Percentage[/b][/td][/tr]')
    print('[tr][td][b]Guild[/b][/td][td][b]{0}[/b][/td][td][b]{1}[/b][/td][td][b]{2}%[/b][/td][/tr]'
          .format(guild_stats['total'], guild_stats['sdps'], guild_stats['pct']))
    for player, player_stats in dpser_dod.items():
        print('[tr][td]{0}[/td][td]{1}[/td][td]{2}[/td][td]{3}%[/td][/tr]'.format(player,
                                                                                  player_stats['sdps'],
                                                                                  player_stats['total'],
                                                                                  player_stats['pct']))
    print('[/table]')