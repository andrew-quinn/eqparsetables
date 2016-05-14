#!/usr/bin/env python3
"""Formats and filters GamParse spells and disc forum output."""

import sys
import argparse
import os
import gpcastreader as gpc
import enjintableprinter as etp
import texttableprinter as ttp
import tableformatter as tf
import parsedb

__author__ = 'Andrew Quinn'
__copyright__ = 'Copyright 2015-2016, Andrew Quinn'
__credits__ = ['Andrew Quinn']
__license__ = 'Simplified BSD'
__version__ = '0.1'
__maintainer__ = 'Andrew Quinn'
__email__ = 'andrew@under.co.nz'
__status__ = 'Prototype'


def main(argv):
    cwd = os.getcwd()
    config_path = cwd + '/config.ini'
    blacklist_path = cwd + '/blacklist.ini'
    input_path = cwd + '/parse.txt'
    dps_first = 1
    dps_last = sys.maxsize
    padding = '\n\n'

    parser = argparse.ArgumentParser(description='Transform GamParse output into you favorite forum table format.')
    parser.add_argument('-p', '--parsefile', help='path to GamParse output', metavar='PATH')
    parser.add_argument('-b', '--blacklist', help='path to blacklist', metavar='PATH')
    parser.add_argument('-c', '--config', help='path to config CSV file', metavar='PATH')
    parser.add_argument('--dps', action='store_true', help='force dps formatting')
    parser.add_argument('--tty', action='store_true', help='output text (default is enjin post format)')
    parser.add_argument('-f', '--dpsfirst', help='highest ranking dpser to show', metavar='FIRST')
    parser.add_argument('-l', '--dpslast', help='lowest ranking dpser to show', metavar='LAST')

    args = parser.parse_args()

    if args.parsefile:
        input_path = args.parsefile
    if args.blacklist:
        blacklist_path = args.blacklist
    if args.config:
        config_path = args.config
    if args.dps:
        if args.dpsfirst:
            dps_first = int(args.dpsfirst)
        if args.dpslast:
            dps_last = int(args.dpslast)

    if args.dps:
        reader = gpc.GPDPSReader(input_path, config_path)
        if args.tty:
            ttp.print_dps_table(reader, dps_first, dps_last)
        else:
            etp.print_dps_table(reader, dps_first, dps_last)
    else:
        reader = gpc.GPCastReader(input_path, config_path, blacklist_path)
        pdb = parsedb.ParseDB(reader.get_spells_cast_by_class(), reader.classes, reader.caster_dod, reader.config)
        if args.tty:
            for i, eq_class in enumerate(sorted(reader.classes)):
                if i:
                    print(padding)
                tf.print_table(tf.format_tty_table(pdb.get_cast_table(eq_class)))
        else:
            for i, eq_class in enumerate(sorted(reader.classes)):
                if i:
                    print(padding)
                tf.print_table(tf.format_enjin_table(pdb.get_cast_table(eq_class)))


if __name__ == '__main__':
    main(sys.argv[1:])
