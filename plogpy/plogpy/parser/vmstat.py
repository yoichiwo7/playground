import collections

import pandas as pd

from plogpy.parser.common import PerfLogParser, LogRegisterInfo

# TODO:
# [x] vmstat
# [x] vmstat -a (active/inactive)
# [ ] vmstat -d (disk)
# [ ] vmstat -t (use timestamp) ???


class VmstatLogParser(PerfLogParser):
    @staticmethod
    def regiter_info():
        return LogRegisterInfo(
            log_type="vmstat (  | -a)", patterns=[r"procs .*?-memory-.*"]
        )

    def parse(self, path) -> pd.DataFrame:
        with open(path) as f:
            multi_level_cols = self.__parse_headers(f)
            df = self.__parse_data(f, multi_level_cols)
        return df

    def __parse_data(self, f, multi_level_cols) -> pd.DataFrame:
        rows = []
        for line in f:
            line = line.strip()
            elems = line.split()
            if elems[0] in multi_level_cols[0]:
                continue
            values = [float(e) for e in elems]
            rows.append(values)
        df = pd.DataFrame(rows, columns=pd.MultiIndex.from_tuples(multi_level_cols))
        return df

    def __parse_headers(self, f):
        category_line = f.readline().strip()
        header_line = f.readline().strip()

        # calculate category range
        category_table = {}
        category = ""
        start_pos = 0
        for pos, char in enumerate(category_line, 0):
            category += char
            if pos == len(category_line) - 1 or char == " ":
                category = category.replace("-", "").strip()
                category_table[category] = (start_pos, pos)
                category = ""
                start_pos = pos + 1

        # category and headers
        d = collections.OrderedDict()
        header = ""
        for pos, char in enumerate(header_line, 0):
            if not char.isspace():
                header += char
            if not (len(header) > 0 and (pos == len(header_line) - 1 or char == " ")):
                continue
            for cat, (start_pos, end_pos) in category_table.items():
                if cat not in d:
                    d[cat] = []
                if start_pos <= pos <= end_pos:
                    d[cat].append(header)
            header = ""

        # generate MultiIndex columns
        multi_level_cols = []
        for cat, headers in d.items():
            for hdr in headers:
                multi_level_cols.append((cat, hdr))
        return multi_level_cols
