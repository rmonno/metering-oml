import threading
import time
import random
import string
import requests
from abc import ABCMeta, abstractmethod
from oml4py import OMLBase


class Agent(threading.Thread):
    __metaclass__ = ABCMeta

    @abstractmethod
    def define_measurements(self):
        pass

    @abstractmethod
    def action(self):
        pass

    def __init__(self, name, domain, id_, collector, interval, logger=None):
        threading.Thread.__init__(self, name=name)
        self.__mutex = threading.Lock()
        self.__stop = threading.Event()
        self.__logger = logger
        self.__interval = int(interval)
        self.daemon = True
        self.oml = OMLBase(name, domain, id_, collector)
        self.start()

    def loop(self, secs):
        while self.is_alive():
            self.join(secs)

    def run (self):
        self.__debug("Run agent base object")
        self.define_measurements()
        self.oml.start()
        try:
            while self.__isStopped() == False:
                self.action()

                self.__debug("Waiting %dsecs before perform an action" %
                             (self.__interval,))
                time.sleep(self.__interval)

        except Exception as e:
            self.error("Run error: %s" % (str(e),))

        finally:
            self.__debug("close communication to collector")
            self.oml.close()

    def stop(self):
        with self.__mutex:
            self.__stop.set()

    def info(self, msg):
        if self.__logger:
            self.__logger.info(msg)

    def error(self, msg):
        if self.__logger:
            self.__logger.error(msg)

    def __debug(self, msg):
        if self.__logger:
            self.__logger.debug(msg)

    def __isStopped(self):
        with self.__mutex:
            return self.__stop.isSet()


class TestAgent(Agent):
    """ Test AGENT class"""
    def __init__(self, app_name, app_domain, app_id, collector_url,
                 mp_name, interval, logger=None):
        super(TestAgent, self).__init__(app_name,
                                        app_domain,
                                        app_id,
                                        collector_url,
                                        interval,
                                        logger)
        self.mp_name = mp_name
        self.info("TestAgent name=%s" % (self.mp_name,))

    def define_measurements(self):
        ms_format_ = "freq:string amplitude:int32"
        self.oml.addmp(self.mp_name, ms_format_)
        self.info("%s: defined measurements format=%s" % (self.mp_name, ms_format_))

    def action(self):
        data_ = [''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(32)]),
                 random.randint(0,100)]
        self.oml.inject(self.mp_name, data_)
        self.info("%s: sent data to collector=%s" % (self.mp_name, data_))


class XenServerAgent(Agent):
    """ XenServer AGENT class"""
    def __init__(self, app_name, app_domain, app_id, collector_url,
                 mp_name, interval, addr, user, pswd, logger=None):
        super(XenServerAgent, self).__init__(app_name,
                                             app_domain,
                                             app_id,
                                             collector_url,
                                             interval,
                                             logger)
        self.mp_name = mp_name
        self.url = 'http://' + addr + '/rrd_updates'
        self.auth = (user, pswd)
        self.interval = int(interval)
        self.info("XenServerAgent name=%s, url=%s, auth=%s" %
                  (self.mp_name, self.url, self.auth,))

    def define_measurements(self):
        self.error('Not implemented yet')

    def action(self):
        try:
            start_ = int(round(time.time())) - self.interval
            resp_ = requests.get(url=self.url,
                                 auth=self.auth,
                                 params={'start': start_})
            self.info("%s: response=%s" % (self.mp_name, resp_.text))

        except requests.exceptions.RequestException as e:
            self.error(str(e))
