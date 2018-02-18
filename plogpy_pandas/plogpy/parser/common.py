import abc
import collections
import re

from plogpy.type import LogType


# chart
#   - name = "CPU Usage"
#   - nodes = all, cpu0, cpu1
#   - dataset_per_node = {"usr": [...], "sys": [...]}
#   - statistics_of_node/dataset = all->usr, all->sys, cpu0->usr, cpu->sys, ..
#      (ex. max, min, average, mean, std-dev, dev, 0/25/50/75/99percentile)

class ParsedPerfData(object):
    def __init__(self):
        self.name = ""
        self.nodes = collections.OrderedDict()  #TODO: statistics(ex. max, min, average)
    
    def __repr__(self):
        return self.name + ":" + str(self.nodes)


class PerfLogParser(abc.ABC):
    @abc.abstractmethod
    def parse(self, path: str) -> collections.OrderedDict:
        pass


from plogpy.parser.dstat import DstatLogParser
from plogpy.parser.sar import SarCpuLogParser

# key=log_type, value=(pattern, parser)
LOG_PARSER_DICT = {
    LogType.DSTAT: (r'Dstat \d+\.\d+.\d+ CSV output', DstatLogParser()),
    LogType.SAR_CPU: (r'CPU\s+\%user\s+\%nice\s+\%system\s+\%iowait\s+\%steal\s+\%idle', SarCpuLogParser()),
    LogType.SAR_CPU_ALL: (r'CPU\s+\%usr\s+\%nice\s+\%sys\s+', SarCpuLogParser()),
}

def get_matched_parser(target_file: str) -> PerfLogParser:
    log_type = __detect_log_type(target_file)
    return get_parser(log_type)


def __detect_log_type(target_file: str, scan_line_num: int = 5) -> LogType:
    with open(target_file) as f:
        for i, line in enumerate(f):
            if i == scan_line_num:
                break
            for log_type, (pattern, _) in LOG_PARSER_DICT.items():
                if re.search(pattern, line):
                    return log_type
    raise Exception("No matched type found:" + target_file)


def get_parser(log_type: LogType) -> PerfLogParser:
    if log_type in LOG_PARSER_DICT:
        _, parser = LOG_PARSER_DICT.get(log_type)
        return parser
    raise Exception("Undefined log type:" + str(log_type))
