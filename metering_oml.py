#!/usr/bin/env python

import sys
import os
import argparse

if __name__ == '__main__':
    bp_ = os.path.dirname(os.path.dirname(os.path.abspath(sys.argv[0])))
    if bp_ not in [os.path.abspath(x) for x in sys.path]:
        sys.path.insert(0, bp_)

import utilities as utils
LOG = None

def main(argv=None):
    if not argv:
        argv = sys.argv

    try:
        bug_reporter_ = '<r.monno@nextworks.it>'
        parser_ = argparse.ArgumentParser(description='Metering OML agents module',
                                          epilog='Please, report bugs to ' + bug_reporter_,
                                          formatter_class=argparse.ArgumentDefaultsHelpFormatter)

        parser_.add_argument('-d', '--debug',
                             default=False,
                             action='store_true',
                             dest='debug',
                             help='set logging level to DEBUG')

        parser_.add_argument('-c', '--config_file',
                             default='metering.xml',
                             help='set configuration file')

        results_ = parser_.parse_args()

    except Exception as ex:
        print 'Got an Exception parsing flags/options:', ex
        return False

    LOG = utils.ColorLog(name='metering_oml', debug=results_.debug)
    LOG.info("%s" % (results_,))


if __name__ == '__main__':
    sys.exit(main())
