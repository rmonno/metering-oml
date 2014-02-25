from termcolor import colored
import logging
import xml.etree.ElementTree as ET


class ColorLog(object):
    colormap = dict(
        debug=dict(color='grey', attrs=['bold']),
        info=dict(color='green', attrs=['bold']),
        warning=dict(color='yellow', attrs=['bold']),
        error=dict(color='red', attrs=['bold']),
        critical=dict(color='magenta', attrs=['bold']),)

    def __init__(self, name, debug):
        self._logger = logging.getLogger(name)
        if debug:
            self._logger.setLevel(logging.DEBUG)
        else:
            self._logger.setLevel(logging.INFO)

        form = logging.Formatter('[%(asctime)-15s] [%(levelname)s] %(message)s')
        screen_hdlr = logging.StreamHandler()
        screen_hdlr.setFormatter(form)
        self._logger.addHandler(screen_hdlr)

    def __getattr__(self, name):
        if name in ['debug', 'info', 'warning', 'error', 'critical']:
            return lambda s, * args: getattr(self._logger, name)(
                colored(str(s), **self.colormap[name]), *args)

        return getattr(self._logger, name)


class ConfigParser(object):
    def __init__(self, cfile, atype):
        tree = ET.parse(cfile)
        root = tree.getroot()
        self.data = {'domain': root.attrib.get('domain'),
                     'id': root.attrib.get('id'),
                     'collectors': [],}

        for colls_ in root.iter('collect'):
            self.data['collectors'].append(colls_.attrib.get('url'))

        for streams_ in root.iter('stream'):
            if streams_.attrib.get('type') == atype:
                self.data['name'] = streams_.attrib.get('mp')
                self.data['interval'] = streams_.attrib.get('interval')

                if streams_.attrib.get('type') == 'xenserver':
                    self.data['address'] = streams_.findtext('address')
                    self.data['user'] = streams_.findtext('user')
                    self.data['pswd'] = streams_.findtext('pswd')

                if streams_.attrib.get('type') == 'enoxcontroller':
                    self.data['address'] = streams_.findtext('address')
                    self.data['port'] = streams_.findtext('port')

                if streams_.attrib.get('type') == 'odlcontroller':
                    self.data['address'] = streams_.findtext('address')
                    self.data['port'] = streams_.findtext('port')
                    self.data['user'] = streams_.findtext('user')
                    self.data['pswd'] = streams_.findtext('pswd')

    def __str__(self):
        return "%s" % (self.data)
