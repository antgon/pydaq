#! /usr/bin/env python3
# coding=utf-8
#
# Copyright (c) 2016-2017 Antonio González
#
# This file is part of pydaq.
#
# Pydaq is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your
# option) any later version.
#
# Pydaq is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
# for more details.
#
# You should have received a copy of the GNU General Public License
# along with pydaq. If not, see <http://www.gnu.org/licenses/>.

import sys

if (sys.version_info.major < 3) or (sys.version_info.minor < 5):
    sys.exit('PyDaq requires Python 3.5 or greater; ' +
             'you are using {}.{}'.format(sys.version_info.major,
                                          sys.version_info.minor))

def main():
    '''
    Arguments:
        --no-gui false -g=false
        --config -c <configfile.yaml> # required if --no-gui
        --output -o <outfile.edf> # required if --no-gui

    Defaults
        --gui true
        --config none
        --output none
    '''
    import argparse
    parser = argparse.ArgumentParser(
            description='PyDAQ: Acquire data from a microcontroller',
            allow_abbrev=False)

    # GUI option: Launch a graphical interface.
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--gui', dest='gui', action='store_true')
    group.add_argument('--no-gui', dest='gui', action='store_false',
                       help='launch (default)/do not launch graphical '+
                       'interface')
    parser.set_defaults(gui=True)

    # File output.
    parser.add_argument('-o', '--output', type=str,
                        help='output EDF file (required if `--no-gui`)')

    # Configuration file.
    parser.add_argument('-c', '--config', type=str,
                        help='configuration file ' +
                        '(required if `--no-gui`)')

    args = parser.parse_args()


    print('GUI: ', args.gui)
    if args.config:
        print('config: ', args.config)
    if args.output:
        print('output: ', args.output)

    if args.gui is True:
        import sys
        from PyQt5 import QtWidgets
        from mainwindow import MainWindow
        app = QtWidgets.QApplication([])
        self = MainWindow()
        self.show()
        sys.exit(app.exec_())
        #QtWidgets.QApplication.instance().exec_()

if __name__ == "__main__":
    main()
