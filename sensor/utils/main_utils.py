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


def write_yaml_file(yaml_file_path: str, data: dict, replace: bool = False) -> dict:
    """
    write dictionary to yaml file
    """
    try:
        if replace:
            if os.path.exists(yaml_file_path):
                os.remove(yaml_file_path)
        os.makedirs(os.path.dirname(yaml_file_path), exist_ok=True)
        with open(yaml_file_path, "w") as yaml_file:
            yaml.dump(data, yaml_file)
    except Exception as e:
        raise SensorException(e, sys)


# saving numpy array data that we get after data transformation
def save_numpy_array(numpy_array: np.array, file_path: str) -> None:
    """
    save numpy array to a file path
    """
    try:

        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, "wb") as file:
            np.save(file, numpy_array)

    except Exception as e:
        raise SensorException(e, sys)


def load_numpy_array(file_path: str):
    """
    load numpy array from file
    """
    try:
        with open(file_path, "rb") as file:
            return np.load(file, allow_pickle=True)
    except Exception as e:
        raise SensorException(e, sys)


def save_python_object(python_object: object, file_path: str):
    """
    save python object to file
    """
    try:
        logging.info(
            f"Entered to method: save_python_object in main_utils and Saving object to {file_path}")

        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, "wb") as file:
            dill.dump(python_object, file)

        logging.info("Exited from method: save_python_object in main_utils")
    except Exception as e:
        raise SensorException(e, sys)


def load_python_object(file_path: str):
    """
    load python object from file
    """
    try:
        if not os.path.exists(file_path):
            raise Exception(f"File {file_path} does not exist")
        with open(file_path, "rb") as file:
            return dill.load(file)
    except Exception as e:
        raise SensorException(e, sys)
