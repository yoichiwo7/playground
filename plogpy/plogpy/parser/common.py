import abc
import importlib
import os
import pkgutil
import re

import pandas as pd

from plogpy.type import LogType


class NoMatchedError(Exception):
    pass


class LogRegisterInfo:
    def __init__(self, log_type, patterns):
        self.log_type = log_type
        self.patterns = patterns


class PerfLogParser(abc.ABC):
    """
    Base class of parser.
    Each log parser class must inherit this class.
    """

    @staticmethod
    @abc.abstractmethod
    def regiter_info() -> LogRegisterInfo:
        """
        (unique_log_type, [regex, ...])
        """
        raise NotImplementedError

    @abc.abstractmethod
    def parse(self, path: str) -> pd.DataFrame:
        """
        Parse file of specifed path.
        Returns pd.DataFrame.
        """
        raise NotImplementedError


# key=id, value=([regex,...], parser)
LOG_PARSER_DICT = {}
regexes_set = set()


def __init_log_parsers():
    parser_classes = __get_parser_classes()
    for cls_ref in parser_classes:
        reg_info = cls_ref.regiter_info()
        log_type = reg_info.log_type
        patterns = reg_info.patterns
        # Check duplication
        if log_type in LOG_PARSER_DICT:
            raise Exception(f"Log type '{log_type}' already exists.")
        # Add log a parser entry
        LOG_PARSER_DICT[log_type] = (patterns, cls_ref())
        for pattern in patterns:
            for t, rs in LOG_PARSER_DICT.items():
                if pattern in rs:
                    raise Exception(
                        f"Duplicated '{pattern}'. Log type=({log_type}, {t})"
                    )
            regexes_set.add(pattern)


# TODO: common.py is not suitable root path for checking parser classes???
def __get_parser_classes() -> list:
    """
    Collect list of PerfLogParser class from current path of the module (that is common.py).
    """
    # get modules
    path = os.path.dirname(__file__)
    mod_names = [modname for _, modname, _ in pkgutil.iter_modules(path=[path])]
    modules = [
        importlib.import_module("." + modname, __package__) for modname in mod_names
    ]

    # get parser classes in each module
    parser_classes = []
    for module in modules:
        class_names = dir(module)
        for classname in class_names:
            cl = getattr(module, classname)
            if __is_parser_class(cl):
                parser_classes.append(cl)
    return parser_classes


def __is_parser_class(class_ref) -> bool:
    """
    Check if the class is the subclass of PerLogParser
    """
    try:
        if issubclass(class_ref, PerfLogParser) and class_ref is not PerfLogParser:
            return True
    except TypeError:
        pass
    return False


def get_matched_parser(target_file: str) -> PerfLogParser:
    log_type = __detect_log_type(target_file)
    return get_parser(log_type)


def get_supported_list() -> list:
    return sorted(LOG_PARSER_DICT.keys())


def __detect_log_type(target_file: str, scan_line_num: int = 5) -> LogType:
    """
    Scan the target_file until scan_line_num and detect the log type.
    Return LogType.
    Throws Exception if no appropriate log type is found.
    """
    MAX_ONE_LINE_BYTE_NUM = 4096
    with open(target_file) as f:
        i = 0
        while True:
            i += 1
            line = f.readline(MAX_ONE_LINE_BYTE_NUM)
            if i == scan_line_num:
                break
            for log_type, (patterns, _) in LOG_PARSER_DICT.items():
                for pattern in patterns:
                    if re.search(pattern, line):
                        return log_type
    raise NoMatchedError("No matched type found:" + target_file)


def get_parser(log_type: LogType) -> PerfLogParser:
    if log_type in LOG_PARSER_DICT:
        _, parser = LOG_PARSER_DICT.get(log_type)
        return parser
    raise Exception("Undefined log type:" + str(log_type))


__init_log_parsers()
