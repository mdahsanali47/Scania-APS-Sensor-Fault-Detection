import yaml
import os
import sys
import dill
import numpy as np

from sensor.exception import SensorException
from sensor.logger import logging


def read_yaml_file(yaml_file_path:str)->dict:
    """
    read yaml file and return as dictionary
    """
    try:
        with open(yaml_file_path, "rb") as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise SensorException(e, sys)