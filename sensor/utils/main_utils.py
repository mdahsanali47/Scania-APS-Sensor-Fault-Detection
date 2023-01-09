import yaml
import os
import sys
import dill
import numpy as np

from sensor.exception import SensorException
from sensor.logger import logging


def read_yaml_file(yaml_file_path: str) -> dict:
    """
    read yaml file and return as dictionary
    """
    try:
        with open(yaml_file_path, "rb") as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise SensorException(e, sys)


def write_yaml_file(yaml_file_path: str, data: dict)->dict:
    """
    write dictionary to yaml file
    """
    try:
        with open(yaml_file_path, "w") as yaml_file:
            yaml.dump(data, yaml_file)
    except Exception as e:
        raise SensorException(e, sys)
