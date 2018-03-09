import os

import pandas as pd

from .parser.common import get_matched_parser, get_parser
from .type import LogType
from .writer import write_df_to_excel


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


def generate_excel_report(
        input_path: str, output_path: str,
        enable_data_sheet: bool = True,
        enable_stats_sheet: bool = True,
        enable_chart_sheet: bool = True,
        use_png: bool = False,
        each_chart: bool = False) -> None:
    """
    Parse peformance log and generate report.
    Generates report file.
    """
    df = parse_log(input_path)
    writer = pd.ExcelWriter(output_path)
    file_name = os.path.split(output_path)[-1]
    name = os.path.splitext(file_name)[0]
    write_df_to_excel(writer, df, name, 
        enable_data_sheet=enable_data_sheet,
        enable_stats_sheet=enable_stats_sheet,
        enable_chart_sheet=enable_chart_sheet,
        use_png=use_png,
        chart_each=each_chart)
    writer.save()