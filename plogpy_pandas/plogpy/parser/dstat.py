import collections

from plogpy.parser.common import PerfLogParser, ParsedPerfData
from plogpy.util import split_csv_line

class DstatLogParser(PerfLogParser):
    def parse(self, path):
        with open(path) as f:
            parsed_dict = self.__parse_headers(f)
            parsed_dict = self.__parse_data(f, parsed_dict)
        return parsed_dict

    def __parse_data(self, f, input_dict) -> collections.OrderedDict:
        target_dict = collections.OrderedDict(input_dict)
        for line in f:
            elems = split_csv_line(line)
            print(target_dict.values())
            for logdata in target_dict.values():
                for dataset in logdata.nodes.values():
                    dataset.append(elems.pop(0))
            if len(elems) > 0: raise Exception("Bad CSV line: " + line)
        return target_dict

    def __parse_headers(self, f) -> collections.OrderedDict:
        FIRST_HEADER_POS = 6
        SECOND_HEADER_POS = 7
        
        for i, line in enumerate(f, 1):
            if i == FIRST_HEADER_POS:
                headers = split_csv_line(line)
                pass
            elif i == SECOND_HEADER_POS:
                sub_headers = split_csv_line(line)
                break

        result_dict = collections.OrderedDict()
        for hdr, sub_hdr in zip(headers, sub_headers):
            if len(hdr) > 0:
                key = hdr
                result_dict[key] = ParsedPerfData()
            result_dict[key].nodes[sub_hdr] = []

        return result_dict

