import collections

import pandas as pd

from plogpy.parser.common import PerfLogParser
from plogpy.util import split_csv_line

class MeminfoLogParser(PerfLogParser):

    @staticmethod
    def regiter_info():
        return ("/proc/meminfo", 
            [
                r'MemTotal:\s+\d+'
            ])

    def parse(self, path):
        with open(path) as f:
            headers = self.__parse_headers(f)
            headers_with_same_parent = [(hdr, hdr) for hdr in headers]
            f.seek(0)
            df = self.__parse_data(f, headers_with_same_parent)
        return df

    def __parse_data(self, f, multi_level_headers):
        entry_num = len(multi_level_headers)
        rows = []
        row_entries = []
        for line_num, line in enumerate(f, 1):
            value = int(line.split()[1])
            row_entries.append(value)

            if line_num % entry_num == 0:
                # move to next meminfo row
                rows.append(row_entries)
                row_entries = []
        df = pd.DataFrame(rows, columns=pd.MultiIndex.from_tuples(multi_level_headers))
        return df

    def __parse_headers(self, f) -> list:
        #TODO: check timestamp line if it exists?
        headers = []
        for line in f:
            keyvalue = line.split(": ")
            if len(keyvalue) != 2:
                raise Exception(f"Unkown line found: {line}")
            hdr = keyvalue[0]
            if hdr in headers:
                # collected all existing headers
                break
            headers.append(hdr)
        return headers
