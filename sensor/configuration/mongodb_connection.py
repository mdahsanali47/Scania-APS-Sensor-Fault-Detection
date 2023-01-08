import os
import sys

import certifi
import pymongo

from sensor.constant.database import DATABASE_NAME
from sensor.constant.env_variable import MONGODB_URL_KEY
from sensor.exception import SensorException

ca = certifi.where()


class MongoDBClient:
    client = None

    def __init__(self, database_name=DATABASE_NAME):
        try:
            if MongoDBClient.client is None:
                monogdb_url = os.environ.get(MONGODB_URL_KEY)
                if monogdb_url is None:
                    raise SensorException(
                        "MongoDB URL is not set in env variable")
                MongoDBClient.client = pymongo.MongoClient(
                    monogdb_url, tlsCAFile=ca)

                self.client = MongoDBClient.client
                self.database = self.client[database_name]
                self.database_name = database_name
        except Exception as e:
            raise SensorException("error in MongoDBClient", sys) from e
