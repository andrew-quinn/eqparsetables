import re

import casttable


class GPCastReader:
    """
    Read and store GamParse caster output information
    """

    def __init__(self, player_data):
        """
        Create a GPCastReader object.

        :param player_data: a container of player information (name, class, alias)
        :param blocklist: a blocklist object containing spells to be ignored
        """
        self.mob = ''
        self.date = ''

        self.player_data = player_data

        self.rk = re.compile(r' (?:Rk\. )?(?:X{0,3})(?:IX|IV|V?I{0,3})$')

    def read_entry_header(self, gp_header, name_grabber, line):
        """
        Read and extract data from a GamParse spell cast entry header.

        :param gp_header: regex for parsing the main header of the cast output
        :param name_grabber: regex for parsing the entry headers of the cast output
        :param line: line of the cast output file to be parsed
        :return: the name of the player casting, if applicable, or 'unknown' if not applicable
        """
        player = 'unknown'
        m = gp_header.match(line[3:-4])
        n = name_grabber.match(line)
        if m:
            self.mob = m.group('mob')
            self.date = m.group('date')
            pass
        elif n:
            player = n.group('name')
            if not self.player_data.is_player(player) and player != 'Total':
                print('Unrecognized player {0}. Please update your config file.'.format(player))
                player = 'unknown'
        return player

    def get_caster_stats(self, caster, lines):
        gp_bullet = '   --- '

        stats = {'name': caster}
        for line in lines:
            if line.startswith(gp_bullet):
                scc = line[len(gp_bullet):].split(" - ")
                spell = self.rk.sub('', scc[0])
                if spell in stats:
                    print(('Spell {0} already exists for {1} with cast count {2}... '
                           'incrementing by {3}').format(spell, caster, stats[spell], scc[1]))
                    stats[spell] = str(int(stats[spell]) + int(scc[1]))
                else:
                    stats.update({spell: scc[1]})
            else:
                return stats

    def init_cast_data(self, input_path):
        """
        Extract caster names and spellcast info from GamParse forum output.

        :return: a dictionary of dictionaries with format
                 stats_list[caster] = {'spell_1': count_1}, ..., {'spell_n': count_n}
        """
        caster = 'unknown'
        gp_header = re.compile(r'(?P<mob>(?:Combined: )?(?:[\w`,]+ ?)+) on (?P<date>\d{1,2}/\d{1,2}/\d{2,4})')
        name_grabber = re.compile(r'\[B\](?P<name>\w+) - \d+\[/B\]')

        stats_list = []
        lines = read_raw_parse(input_path)
        for i, line in enumerate(lines):
            if line.upper().startswith('[B]'):
                caster = self.read_entry_header(gp_header, name_grabber, line)
                if caster == 'unknown':
                    continue
                stats_list.append(self.get_caster_stats(caster, lines[i+1:]))

        return stats_list

    def get_cast_table(self, input_path, blocklist):
        """
        Combine all player spellcast info with player data.

        :return: a data frame of spells X casters
        """
        spellcasts = self.init_cast_data(input_path)
        return casttable.CastTable(spellcasts, self.player_data, blocklist)


def read_raw_parse(path):
    """
    Read GamParse's forum output into a list.

    :param path: path to a file containing GamParse output
    :return: a list containing the lines of the input file
    """
    with open(path, 'r') as input_handle:
        return input_handle.read().splitlines()
