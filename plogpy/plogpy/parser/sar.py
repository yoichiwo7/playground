import collections

import pandas as pd

from plogpy.parser.common import PerfLogParser

class SarLogParser(PerfLogParser):

    @staticmethod
    def regiter_info():
        return ("sar", 
            [
                r'CPU\s+\%user\s+\%nice\s+\%system\s+\%iowait\s+\%steal\s+\%idle',
                r'CPU\s+\%usr\s+\%nice\s+\%sys\s+'
            ])

    def parse(self, path):
        with open(path) as f:
            node_type, cols = self.__parse_header(f)
            df= self.__parse_data(f, node_type, cols)
            return df

    def __parse_data(self, f, node_type, cols):
        #TODO: return multi-level-cols-df instead of dictionary
        dataset_dict = collections.OrderedDict()
        for line in f:
            elems = self.__parse_sar_line(line)
            if len(elems) == 0 or (len(elems) > 1 and elems[1] == node_type):
                #TODO: ignore AVG:
                continue
            print(elems, node_type)
            if node_type:
                node = elems[1]
                pos = 2
            else:
                node = "system"
                pos = 1
            nums = [float(e)  for e in elems[pos:]]
            l = dataset_dict.setdefault(node, [])
            l.append(nums)
        
        nodes = dataset_dict.keys()
        dfs = []
        for node in nodes:
            node_cols = [ (f"{node_type}:{node}", col) for col in cols]
            df = pd.DataFrame(dataset_dict[node], columns=pd.MultiIndex.from_tuples(node_cols))
            dfs.append(df)
        
        final_df = dfs.pop(0)
        for df in dfs:
            final_df = pd.concat([final_df, df], axis=1)
        
        return final_df

    def __parse_header(self, f) -> (str, list):
        f.readline()
        for line in f:
            elems = self.__parse_sar_line(line)
            if len(elems) > 1:
                if elems[1].isupper():
                    node_type = elems[1]
                    headers = elems[2:]
                else:
                    node_type = None
                    headers = elems[1:]
                return node_type, headers
        raise Exception("Header line not found.")

    def __parse_sar_line(self, line):
        line = line.replace("\n", "").replace("\r", "")
        return line.split()


#TODO: check date format
#TODO: check average line
#TODO: unify header line and empty line check process