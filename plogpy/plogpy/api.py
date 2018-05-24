import os

import pandas as pd

from .parser.common import get_matched_parser, get_parser, get_supported_list, NoMatchedError
from .type import LogType
from .writer import HtmlWriter, XlsxWriter, WriterConfig


"""
Public APIs for plogpy
"""

def get_supported_log_types() -> list:
    return get_supported_list()


#TODO: checks all pattern twice (is_parsable and parse_log) -> make it more efficient in future.
def is_parsable(input_path: str) -> bool:
    try:
        get_matched_parser(input_path)
        return True
    except NoMatchedError:
        return False


def parse_log(input_path: str, log_type: LogType = LogType.AUTO_DETECTION) -> pd.DataFrame:
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
        max_samples: int = None,
        enable_data_sheet: bool = True,
        enable_stats_sheet: bool = True,
        enable_chart_sheet: bool = True,
        each_chart: bool = False) -> None:
    """
    Parse peformance log and generate report.
    Generates report file.
    """
    df = parse_log(input_path)
    
    writer = pd.ExcelWriter(output_path)
    file_name = os.path.split(output_path)[-1]
    name = os.path.splitext(file_name)[0]
    report_writer = XlsxWriter(
        writer_config=WriterConfig(chart_type_foreach=("line", "unstacked"))
    )
    report_writer.write_df_to_excel(writer, df, name, 
        max_samples=max_samples,
        enable_data_sheet=enable_data_sheet,
        enable_stats_sheet=enable_stats_sheet,
        enable_chart_sheet=enable_chart_sheet,
        chart_each=each_chart) 
    writer.save()


def generate_html_report(
    input_path: str,
    output_path: str,
    max_samples: int = None
) -> None:
    df = parse_log(input_path)
    with open(output_path, "w") as writer:
        report_writer = HtmlWriter()
        report_writer.write_df_to_html(df, writer, max_samples=max_samples)


#TODO: Need to process as javascript too. (Currently no chartjs in Notebook)
def show(input_path, max_samples=512):
    empty_writer = None
    df = parse_log(input_path)
    report_writer = HtmlWriter()
    from IPython.display import display, HTML
    html_str = report_writer.write_df_to_html(df, empty_writer, max_samples=max_samples)
    display(HTML(html_str))


def generate_json(input_path: str, stats: bool) -> dict:
    """
    Generates JSON dictionary from log file.
    Example:
    {
        "index": [1,2,3,4,5],
        "column": ["read", "write"],
        "values": {
            "read" : [100, 20, 30, 0, 50],
            "write": [200, 40, 10, 5, 35]
        }
    }
    """
    d = {}
    df = parse_log(input_path)
    if stats:
        d["stats"] = {}
        __put_json_object(df.describe(), d["stats"])
    d["data"] = {}
    __put_json_object(df, d["data"])
    return d


def __put_json_object(df, d):
    #TODO: not suited for large data. make it more efficient?
    columns = df.columns.tolist()
    d["index"] = df.index.tolist()
    d["column"] = [str(col) for col in columns]
    d["values"] = { str(col):df[col].values.tolist() for col in columns}
