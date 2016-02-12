#!/usr/bin/env python

import sys
import threading
import time
import random
import string as S
from oml4py import OMLBase

DOMAIN = 'ocf-measurement-oml'
IDENTIFIER = 'omlc-monroe-test'
APPLICATION_NAME = 'TestOmlClient'
MEASUREMENT_POINT_NAME = 'MONROEmp1'
URL = 'tcp:%s:%s' % ("213.182.68.136", "3003")


class TestOmlClient(threading.Thread):
    def __init__(self, interval=10):
        threading.Thread.__init__(self, name=APPLICATION_NAME)
        self.__mutex = threading.Lock()
        self.__stop = threading.Event()
        self.__interval = int(interval)
        self.daemon = True
        self.oml = OMLBase(APPLICATION_NAME, DOMAIN, IDENTIFIER, URL)
        self.start()

    def define_measurements(self):
        msformat = "freq:string amplitude:int32"
        self.oml.addmp(MEASUREMENT_POINT_NAME, msformat)
        print "%s: defined measurements format=%s" %\
            (MEASUREMENT_POINT_NAME, msformat)

    def action(self):
        tmp = [random.choice(S.ascii_letters + S.digits) for n in xrange(32)]
        data = [''.join(tmp), random.randint(0, 100)]
        self.oml.inject(MEASUREMENT_POINT_NAME, data)
        print "%s: sent data to collector=%s" % (MEASUREMENT_POINT_NAME, data)

    def run(self):
        print 'Run TestOmlClient'
        self.define_measurements()
        self.oml.start()
        try:
            while self.__isStopped() is False:
                self.action()
                print 'Waiting %dsecs' % (self.__interval)
                time.sleep(self.__interval)

        except Exception as e:
            print "Run error: %s" % str(e)
        finally:
            print "close communication to collector"
            self.oml.close()

    def loop(self, secs):
        while self.is_alive():
            self.join(secs)

    def stop(self):
        with self.__mutex:
            self.__stop.set()

    def __isStopped(self):
        with self.__mutex:
            return self.__stop.isSet()


def main(argv=None):
    if not argv:
        argv = sys.argv

    client = TestOmlClient()
    try:
        print "Start collecting measurements..."
        client.loop(secs=10)

    except KeyboardInterrupt:
        print 'Interrupt'
        client.stop()

    except Exception as ex:
        print 'Got an Exception: %s' % (ex)
        return False

    client.join(timeout=10)

    print 'bye bye..'
    return True


if __name__ == '__main__':
    sys.exit(main())
