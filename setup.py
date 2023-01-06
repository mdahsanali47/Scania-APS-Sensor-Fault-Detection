from setuptools import setup, find_packages
from typing import List
# Declaring variables for setup function

PROJECT_NAME = 'Scania_APS_Sensor'
VERSION = '0.0.2'
AUTHOR = 'Md Ahsan Ali'
AUTHOR_EMAIL = 'mdahsanali47@gmail.com'
DESCRIPTION = 'A package for Scania APS sensor Fault Detection'
LONG_DESCRIPTION = """
                    Scania APS sensor Fault Detection and reduce the cost of unnecessary repairs.
                    The benefits of using an APS instead of a hydraulic system are the easy availability and long-term sustainability of natural air.
                    """
REQUIREMENTS_FILE_NAME = 'requirements.txt'
HYPHEN_E_DOT = '-e .'

def get_requirements_list() ->List[str]:
    """
    Description: This function is going to return list of requirement
    mention in requirements.txt file
    Return: This function is going to return a list which contain name
    of libraries mentioned in requirements.txt file
    """
    with open(REQUIREMENTS_FILE_NAME) as requirement_file:
        requirement_list = requirement_file.readlines()
        requirement_list = [requirement_name.replace('\n', '') for requirement_name in requirement_list]
        if HYPHEN_E_DOT in requirement_list:
            requirement_list.remove(HYPHEN_E_DOT)
    return requirement_list

setup(
    name=PROJECT_NAME,
    version=VERSION,
    author=AUTHOR,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    author_email=AUTHOR_EMAIL,
    packages=find_packages(),
    install_requires=get_requirements_list()
)