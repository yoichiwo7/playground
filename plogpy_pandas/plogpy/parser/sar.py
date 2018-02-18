import collections

from plogpy.parser.common import PerfLogParser, ParsedPerfData

class SarCpuLogParser(PerfLogParser):
    def parse(self, path):
        with open(path) as f:
            headers = self.__parse_header(f)
            logdata = self.__parse_data(f, headers)
            return collections.OrderedDict({"CPU Usage": logdata})

    def __parse_data(self, f, headers):
        logdata = ParsedPerfData()
        for line in f:
            elems = self.__parse_sar_line(line)
            if len(elems) == 0 or (len(elems) > 1 and elems[1] == "CPU"):
                continue
            node = elems[1]
            nums = elems[2:]
            if node not in logdata.nodes:
                d = collections.OrderedDict()
                for hdr in headers:
                    d[hdr] = []
                logdata.nodes[node] = d
            nodeMap = logdata.nodes[node]
            for h, n in zip(headers, nums):
                nodeMap[h].append(n)
        return logdata


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