from configparser import ConfigParser


configure = ConfigParser()
configure.read('config.cfg')


def get(key, value):
    return configure.get(key, value)


def getint(key, value):
    return configure.getint(key, value)
