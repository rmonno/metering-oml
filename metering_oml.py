#!/usr/bin/env python

import sys
import os
import argparse

if __name__ == '__main__':
    bp_ = os.path.dirname(os.path.dirname(os.path.abspath(sys.argv[0])))
    if bp_ not in [os.path.abspath(x) for x in sys.path]:
        sys.path.insert(0, bp_)

import utilities as utils
import agents
LOG = None

def main(argv=None):
    if not argv:
        argv = sys.argv

    try:
        bug_reporter_ = '<r.monno@nextworks.it>'
        parser_ = argparse.ArgumentParser(description='Metering OML agents module',
                                          epilog='Please, report bugs to ' + bug_reporter_,
                                          formatter_class=argparse.ArgumentDefaultsHelpFormatter)

        parser_.add_argument('agent',
                             choices=['flowvisor', 'vm-server'],
                             help='choose the type of agent')

        parser_.add_argument('-d', '--debug',
                             default=False,
                             action='store_true',
                             help='set logging level to DEBUG')

        parser_.add_argument('-c', '--config_file',
                             default='metering.xml',
                             help='set configuration file')

        args_ = parser_.parse_args()

    except Exception as ex:
        print 'Got an Exception parsing flags/options:', ex
        return False

    LOG = utils.ColorLog(name='metering_oml', debug=args_.debug)
    LOG.info("%s" % (args_,))

    configs_ = utils.ConfigParser(args_.config_file, args_.agent)
    LOG.debug("configs=%s" % (str(configs_),))

    if len(configs_.data.get('collectors')) != 1:
        LOG.error("Configuration error: unable to send data to more than one collector!")
        return False

    if args_.agent == 'vm-server' and len(configs_.data.get('vt_ams')) != 1:
        LOG.error("Configuration error (vm-server): unable to retrive data to more than one vt-am!")
        return False

    try:
        agent_ = None
        if args_.agent == 'vm-server':
            agent_ = agents.VTAgent('VTAgent', configs_.data.get('domain'), configs_.data.get('id'),
                                    configs_.data.get('collectors')[0], configs_.data.get('name'),
                                    configs_.data.get('interval'), configs_.data.get('vt_ams')[0], LOG)
            agent_.loop(secs=10)

    except KeyboardInterrupt:
        LOG.warning("User interruption!")
        if agent_:
            agent_.stop()

    except Exception as ex:
        LOG.error("Exception: %s" % (ex,))

    if agent_:
        agent_.join(timeout=10)

    return True

if __name__ == '__main__':
    sys.exit(main())
