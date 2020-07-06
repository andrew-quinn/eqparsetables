import re

import dpstable


class GPDPSReader:
    """
    Read GamParse dps output information and store it for later processing.
    """

    def __init__(self, player_data):
        """
        Construct a GPDPSReader object.

        :param player_data: a container of player information (name, class, alias)
        """
        self.player_data = player_data

        self.mob = 'unknown'
        self.time = 0
        self.date = 'unknown'

    def get_info(self):
        """
        Retrieve a list of dps parse meta-information.

        :return: a list containing mob name, fight time, and fight date
        """
        return [self.mob, self.time, self.date]

    def read_entry_header(self, gp_header, name_grabber, line):
        """
        Read and extract data from a GamParse dps entry header.

        :param gp_header: regex for parsing the main header of the dps output
        :param name_grabber: regex for parsing the entry headers of the dps output
        :param line: line of the dps output file to be parsed
        :return: the name of the player doing the dps, if applicable, or 'unknown' if not applicable
        """
        player = 'unknown'
        m = gp_header.match(line[3:-4])
        n = name_grabber.match(line)
        if m:
            self.mob = m.group('mob')
            self.time = int(m.group('time'))
            self.date = m.group('date')
        elif n:
            player = n.group('name')
            if not self.player_data.is_player(player) and player != 'Total':
                print(f'Unrecognized player {player}. Did you forget to associate a pet with its owner?')
                return 'unknown'
        return player

    def init_dps(self, input_path):
        """
        Extract caster names and spell cast info from GamParse forum output.

        :return: a dictionary of dictionaries associating each dpser with his or her stats
        """
        player = 'unknown'
        gp_header = re.compile(
            r'(?P<mob>(?:Combined: )?(?:[\w`,]+ ?)+) on (?P<date>\d{1,2}/\d{1,2}/\d{2,4}) in (?P<time>\d{1,5})sec')
        name_grabber = re.compile(r'\[B\](?P<name>\w+)\[/B\]')
        dps_grabber = re.compile(
            r'(?P<total>\d+) \@ (?P<sdps>\d+) sdps \((?P<dps>\d+) dps in (?P<time>\d+)s\) \[(?P<pct>\d+(\.\d+)?)%\]')
        dmg_bullet = ' --- [B]DMG:[/B] '

        with open(input_path, 'r') as input_handle:
            lines = input_handle.read().splitlines()

        stats_list = []
        for line in lines:
            if line.upper().startswith('[B]'):
                player = self.read_entry_header(gp_header, name_grabber, line)
                if player == 'unknown' or player == 'Total':
                    continue
            elif line.startswith(dmg_bullet):
                if player == 'unknown' or player == 'Total':
                    continue
                b = dps_grabber.match(line[len(dmg_bullet):])
                stats = {'name': player,
                         'total': b.group('total'),
                         'sdps': b.group('sdps'),
                         'dps': b.group('dps'),
                         'time': b.group('time'),
                         'pct': b.group('pct')}
                stats_list.append(stats)

        return stats_list

    def get_dps_table(self, input_path):
        dps = self.init_dps(input_path)
        return dpstable.DPSTable(dps, self.player_data)
