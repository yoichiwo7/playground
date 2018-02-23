import collections

import pandas as pd

from plogpy.parser.common import PerfLogParser
from plogpy.util import split_csv_line

class DstatLogParser(PerfLogParser):
    def parse(self, path):
        with open(path) as f:
            multi_level_cols = self.__parse_headers(f)
            df_dict = self.__parse_data(f, multi_level_cols)
        return df_dict

    def __parse_data(self, f, multi_level_cols) -> collections.OrderedDict:
        # return dict: key=str('system'), value=pd.DataFrame
        multi_index = pd.MultiIndex.from_tuples(multi_level_cols)
        rows = []
        for line in f:
            elems = split_csv_line(line)
            nums = [float(e) for e in elems]
            if len(nums) != len(multi_level_cols): raise Exception("Bad CSV line: " + line)
            rows.append(nums)
        df = pd.DataFrame(rows, columns=multi_index)
        df_dict = collections.OrderedDict()
        df_dict['system'] = df
        return df_dict

    def __parse_headers(self, f) -> pd.MultiIndex:
        FIRST_HEADER_POS = 6
        SECOND_HEADER_POS = 7
        
        for i, line in enumerate(f, 1):
            if i == FIRST_HEADER_POS:
                headers = split_csv_line(line)
                pass
            elif i == SECOND_HEADER_POS:
                sub_headers = split_csv_line(line)
                break

        multi_level_cols = []
        for hdr, sub_hdr in zip(headers, sub_headers):
            if len(hdr) > 0:
                current_hdr = hdr
            multi_level_cols.append((current_hdr, sub_hdr))
        return multi_level_cols

