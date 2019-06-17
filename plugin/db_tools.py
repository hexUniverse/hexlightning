from configparser import ConfigParser

import logging
import coloredlogs

import redis
from redis.exceptions import ConnectionError

import pymongo
from pymongo.errors import ConnectionFailure

## init ##
config = ConfigParser()
config.read('config.txt')

logger = logging.getLogger(__name__)
coloredlogs.install(level='INFO')


def use_mongo(collection='hexlightning'):
    try:
        client = pymongo.MongoClient(config.get('database', 'mongo'))
    except ConnectionFailure:
        logger.critical('MongoDB Connect Error')
    else:
        return client['hexlightning']


def use_redis():
    try:
        client = redis.from_url(config.get('database', 'redis'))
    except ConnectionError:
        logger.critical('Redis Connect Error')
    else:
        return client
