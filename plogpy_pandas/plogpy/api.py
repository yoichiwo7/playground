from .parser.common import get_matched_parser, get_parser
from .type import LogType


"""
Public APIs for plogpy
"""

def parse_log(input_path: str, log_type: LogType = LogType.AUTO_DETECTION) -> dict:
    """
    Parse performance log.
    Returns dictionary.
    """
    if log_type == LogType.AUTO_DETECTION:
        parser = get_matched_parser(input_path)
    else:
        parser = get_parser(log_type)
    dataframe_dict = parser.parse(input_path)
    return dataframe_dict


def generate_report(input_path: str, output_path: str) -> None:
    """
    Parse peformance log and generate report.
    Generates report file.
    """
    pass