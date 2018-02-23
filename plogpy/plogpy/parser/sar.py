import collections

import pandas as pd

from plogpy.parser.common import PerfLogParser

class SarCpuLogParser(PerfLogParser):
    def parse(self, path):
        with open(path) as f:
            cols = self.__parse_header(f)
            print(cols)
            df_dict = self.__parse_data(f, cols)
            return df_dict

    def __parse_data(self, f, cols):
        dataset_dict = collections.OrderedDict()
        for line in f:
            elems = self.__parse_sar_line(line)
            if len(elems) == 0 or (len(elems) > 1 and elems[1] == "CPU"):
                continue
            node = elems[1]
            nums = [float(e)  for e in elems[2:]]
            l = dataset_dict.setdefault(node, [])
            l.append(nums)
        df_dict = collections.OrderedDict()
        for node, dataset in dataset_dict.items():
            df_dict[node] = pd.DataFrame(dataset, columns=cols)
        return df_dict


    def __parse_header(self, f):
        for line in f:
            elems = self.__parse_sar_line(line)
            if len(elems) > 1 and elems[1] == "CPU":
                headers = elems[2:]
                return headers
        raise Exception("Header line not found.")

    def __parse_sar_line(self, line):
        line = line.replace("\n", "").replace("\r", "")
        return line.split()


#TODO: check date format
#TODO: check average line
#TODO: unify header line and empty line check process