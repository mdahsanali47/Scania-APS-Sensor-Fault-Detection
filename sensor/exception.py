import sys


def error_message_details(error, error_details: sys):

    _, _, exc_tb = error_details.exc_info()
    file_name = exc_tb.tb_frame.f_code.co_filename
    line_number = exc_tb.tb_lineno

    error_message = "Error : [{0}] error occured in file name: [{1}] at line: [{2}]".format(
        error, file_name, line_number)

    return error_message


class SensorException(Exception):
    """Base class for other exceptions"""

    def __init__(self, error_message, error_details: sys):
        super().__init__(error_message)

        self.error_message = error_message_details(
            error_message, error_details=error_details)

    def __str__(self):
        return self.error_message
