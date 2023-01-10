import sys

import numpy as np
from pandas import DataFrame
from typing import Optional

from sensor.exception import SensorException
from sensor.configuration.mongodb_connection import MongoDBClient

from sensor.constant.database import COLLECTION_NAME, DATABASE_NAME


class SensorData:

    """
    Exporting entire MongoDB records in my database_name to panda DataFrame
    """

    def __init__(self):

        try:
            self._mongodb_client = MongoDBClient(database_name=DATABASE_NAME)
        except Exception as e:
            raise SensorException(e, sys)

    def export_data_as_dataframe(self, collection_name: str,
                                 database_name: Optional[str] = None) -> DataFrame:
        """
        Exporting entire MongoDB records in my database_name to panda DataFrame
        :param collection_name:
        :return: pandas dataframe
        """

        try:
            if database_name is None:
                collection = self._mongodb_client.database[collection_name]
            else:
                collection = self._mongodb_client.database[database_name][collection_name]

            df = DataFrame(list(collection.find()))

            if "_id" in df.columns:
                df.drop(columns="_id", inplace=True)

            df = df.replace('na', np.nan)
            return df
        except Exception as e:
            raise SensorException(e, sys)
