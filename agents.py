import threading
import time
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

                self.__debug("Waiting %d before perform an action" %
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


class VTAgent(Agent):
    def __init__(self, app_name, app_domain, app_id, collector_url,
                 mp_name, interval, vt_am, logger=None):
        super(VTAgent, self).__init__(app_name, app_domain, app_id,
                                      collector_url, interval, logger)
        self.mp_name = mp_name
        self.vt_am = vt_am
        self.info("VTAgent name=%s, vt_am=%s" % (self.mp_name, self.vt_am,))

    def define_measurements(self):
        self.info("define measurements")
        self.oml.addmp(self.mp_name, "freq:string amplitude:int32")

    def action(self):
        self.info("send meters to collector")
        self.oml.inject(self.mp_name, ['pippuzzo', 14])
