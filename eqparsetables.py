#!/usr/bin/env python3
"""Formats and filters GamParse spells and disc forum output."""

import argparse
import os
import sys

import castgrapher as cg
import casttable
import enjinformatter
import format
import gamparsecastreader as gpc
import gamparsedpsreader as gpd
import playerdata
import ttyformatter

__author__ = 'Andrew Quinn'
__copyright__ = 'Copyright 2015-2016, Andrew Quinn'
__credits__ = ['Andrew Quinn']
__license__ = 'Simplified BSD'
__version__ = '0.1'
__maintainer__ = 'Andrew Quinn'
__email__ = 'andrew@under.co.nz'
__status__ = 'Prototype'


def get_arg_parser():
    parser = argparse.ArgumentParser(description='Transform GamParse output into your favorite forum table format.')
    parser.add_argument('paths', help='a list of paths containing GamParse output', nargs='*', metavar='PATHS')
    parser.add_argument('-b', '--blocklist', help='path to blocklist', metavar='PATH')
    parser.add_argument('-c', '--config', help='path to config CSV file', metavar='PATH')
    parser.add_argument('--dps', action='store_true', help='force dps formatting')
    parser.add_argument('--tty', action='store_true', help='output text (default is enjin post format)')
    parser.add_argument('--attn', action='store_true', help='reconstruct attendance list')  # Work in progress...
    parser.add_argument('-f', '--dpsfirst', help='highest ranking dpser to show', metavar='FIRST')
    parser.add_argument('-l', '--dpslast', help='lowest ranking dpser to show', metavar='LAST')

    return parser


def main(argv):
    parser = get_arg_parser()
    args = parser.parse_args()

    paths = get_input_paths(args)
    player_data = get_player_data(args)
    make_table = get_table_maker(args)

    if args.dps:
        dps_first, dps_last = get_dps_bounds(args)
        handle_dps(paths, player_data, dps_first, dps_last, make_table)
    else:
        blocked_spells = get_blocklist(args)
        handle_casts(paths, player_data, blocked_spells, make_table)


def get_input_paths(args):
    default_path = os.getcwd() + '/parse.txt'
    paths = list()
    if args.paths:
        for path in args.paths:
            check_file(path)
            paths.append(path)
    else:
        check_default_file(default_path)
        paths.append(default_path)
    return paths


def get_blocklist(args):
    blocklist_path = os.getcwd() + '/blocklist.ini'
    if args.blocklist:
        check_file(args.blocklist)
        blocklist_path = args.blocklist
    else:
        check_default_file(blocklist_path)

    blocklist = []
    with open(blocklist_path, 'r') as bl_handle:
        for row in bl_handle.read().splitlines():
            blocklist.append(row.strip())

    return blocklist


def get_player_data(args):
    config_path = os.getcwd() + '/config.ini'
    if args.config:
        check_file(args.config)
        config_path = args.config
    else:
        check_default_file(config_path)
    return playerdata.PlayerData(config_path)


def get_table_maker(args):
    if args.tty:
        return ttyformatter.make_table
    else:
        return enjinformatter.make_table


def get_dps_bounds(args):
    """
    Get dps placement bounds from args.

    :param args: parsed arguments
    :return: placement indices of the first and last players to be shown
    """
    dps_first = 0
    dps_last = 10

    if args.dpsfirst:
        dps_first = int(args.dpsfirst) - 1
    if args.dpslast:
        dps_last = int(args.dpslast)

    return sorted([0, dps_first, dps_last, sys.maxsize])[1:3]


def check_file(path):
    if not os.path.isfile(path):
        print("Could not find the file {0}. Exiting.".format(path))
        sys.exit()


def check_default_file(path):
    if not os.path.isfile(path):
        answer = input("Could not find the file {0}. Would you like to create a blank version now? [y/N] ".format(path))
        if str(answer).lower() == 'y':
            with open(path, 'a+') as _:
                pass
        else:
            print('Exiting.')
            sys.exit()


def handle_casts(paths, player_data, blocked, make_table):
    """
    Generate formatted spell cast output.

    :param paths: a list of paths to GamParse output
    :param player_data: a PlayerData object
    :param blocked: a Blocklist object of spells to be ignored
    :param make_table: a function: f(eq_class, [[header strings...], ...], [[row strings], ...] -> string
    """
    cast_table = get_cast_table(paths, player_data, blocked)

    padding = '\n\n'
    classes = cast_table.get_classes()
    for i, eq_class in enumerate(sorted(classes)):
        if i > 0:
            print(padding)

        totals = ['Total'] + [str(t) for t in cast_table.get_totals(eq_class)]
        spells, rows = cast_table.get_rows(eq_class)
        cg.generate_class_graphs(spells, rows, eq_class)
        print(make_table(eq_class, [spells, totals], rows))


def get_cast_table(paths, player_data, blocklist):
    """
    Create an aggregated CastTable from GamParse output file(s)

    :param paths: a list of paths to GamParse output
    :param player_data: a PlayerData object
    :param blocklist: a list of spells to be ignored
    :return: a CastTable object
    """
    reader = gpc.GPCastReader(player_data)

    cast_tables = list()
    for path in paths:
        cast_tables.append(reader.get_cast_table(path, blocklist))
    return casttable.aggregate(cast_tables)


def handle_dps(paths, player_data, dps_first, dps_last, make_table):
    """
    Generate formatted dps output.

    :param paths: a list of paths to GamParse output
    :param player_data: a PlayerData object
    :param dps_first: the index of the first player to be shown
    :param dps_last: the index of the last player to be shown
    :param make_table: a function: f(eq_class, [[header strings...], ...], [[row strings], ...] -> string
    """
    dps_table = get_dps_table(paths, player_data)

    headers, rows = dps_table.get_rows()
    if dps_last > len(rows):
        dps_last = len(rows)

    formatted_rows = [[format.humanize(cell) for cell in row] for row in rows]
    print(make_table("DPS", [headers], formatted_rows[dps_first:dps_last]))
    players = dps_table.get_players()
    chart_rows = [[row[1], int(row[3])] for row in rows]
    cg.graph_dps(chart_rows[dps_first:dps_last])


def get_dps_table(paths, player_data):
    if len(paths) > 1:
        print('Combining DPS parses is not currently supported. Ignoring input files {0}...'
              .format(', '.join(paths[1:])))

    path = paths[0]
    reader = gpd.GPDPSReader(player_data)
    dps_table = reader.get_dps_table(path)
    return dps_table


if __name__ == '__main__':
    main(sys.argv[1:])
