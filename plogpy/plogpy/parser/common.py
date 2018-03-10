import abc
import collections
import re

import pandas as pd

from plogpy.type import LogType


class PerfLogParser(abc.ABC):
    @staticmethod
    @abc.abstractmethod
    def regiter_info() -> tuple:
        """
        (unique_log_type, [regex, ...])
        """
        pass

    @abc.abstractmethod
    def parse(self, path: str) -> pd.DataFrame:
        pass


#TODO: load parser dymanically (pkgutil.walk_packages)
from plogpy.parser.dstat import DstatLogParser
from plogpy.parser.sar import SarCpuLogParser
from plogpy.parser.sar import SarDevLogParser
from plogpy.parser.sar import SarEdevLogParser
from plogpy.parser.sar import SarTcpLogParser
from plogpy.parser.sar import SarEtcpLogParser
from plogpy.parser.sar import SarRamLogParser

PARSER_CLASSES = [
    DstatLogParser, SarCpuLogParser, SarDevLogParser, SarEdevLogParser, SarTcpLogParser, SarEtcpLogParser, SarRamLogParser
]

#key=id, value=([regex,...], parser)
LOG_PARSER_DICT = {}
regexes_set = set()
def __init_log_parsers():
    for cls in PARSER_CLASSES:
        log_type, regexes = cls.regiter_info()
        # Check duplication
        if log_type in LOG_PARSER_DICT:
            raise Exception(f"Log type '{log_type}' already exists.")
        # Add log a parser entry
        LOG_PARSER_DICT[log_type] = (regexes, cls())
        for regex in regexes:
            for t, rs in LOG_PARSER_DICT.items():
                if regex in rs:
                    raise Exception(f"Duplicated '{regex}'. Log type=({log_type}, {t})")
            regexes_set.add(regex)


def get_matched_parser(target_file: str) -> PerfLogParser:
    log_type = __detect_log_type(target_file)
    return get_parser(log_type)


def __detect_log_type(target_file: str, scan_line_num: int = 5) -> LogType:
    with open(target_file) as f:
        for i, line in enumerate(f):
            if i == scan_line_num:
                break
            for log_type, (patterns, _) in LOG_PARSER_DICT.items():
                for pattern in patterns:
                    if re.search(pattern, line):
                        return log_type
    raise Exception("No matched type found:" + target_file)


def get_parser(log_type: LogType) -> PerfLogParser:
    if log_type in LOG_PARSER_DICT:
        _, parser = LOG_PARSER_DICT.get(log_type)
        return parser
    raise Exception("Undefined log type:" + str(log_type))


__init_log_parsers()