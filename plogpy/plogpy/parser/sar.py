import collections

import pandas as pd

from plogpy.parser.common import PerfLogParser, LogRegisterInfo

# TODO: sar -n (IP|EIP|UDP|SOCK|ALL)


class SarDiskLogParser(PerfLogParser):
    @staticmethod
    def regiter_info():
        return LogRegisterInfo(
            log_type="sar (sar -d)",
            patterns=[
                r"DEV\s+tps\s+rkB/s\s+wkB/s\s+areq-sz\s+aqu-sz\s+await\s+svctm\s+%util"
            ],
        )

    def parse(self, path):
        parser = SarLogParser()
        df = parser.parse(path)
        multi_cols = [
            ("Transaction", "tps"),
            ("R/W(KB)", "rkB/s"),
            ("R/W(KB)", "wkB/s"),
            ("ReqSize(KB)", "areq-sz"),
            ("ReqQueue", "aqu-sz"),
            ("Wait(ms)", "await"),
            ("ServiceTime(ms)", "svctm"),
            ("Usage(%)", "%util"),
        ]
        return add_group_column(df, multi_cols)


class SarLoadAverageLogParser(PerfLogParser):
    @staticmethod
    def regiter_info():
        return LogRegisterInfo(
            log_type="sar (sar -q)",
            patterns=[r"runq-sz\s+plist-sz\s+ldavg-1\s+ldavg-5\s+ldavg-15\s+blocked"],
        )

    def parse(self, path):
        parser = SarLogParser()
        df = parser.parse(path)
        multi_cols = [
            ("Run Queue", "runq-sz"),
            ("Task List", "plist-sz"),
            ("Load Average(min)", "ldavg-1"),
            ("Load Average(min)", "ldavg-5"),
            ("Load Average(min)", "ldavg-15"),
            ("Blocked", "blocked"),
        ]
        return add_group_column(df, multi_cols)


class SarSysLogParser(PerfLogParser):
    @staticmethod
    def regiter_info():
        return LogRegisterInfo(log_type="sar (sar -w)", patterns=[r"proc/s\s+cswch/s"])

    def parse(self, path):
        parser = SarLogParser()
        df = parser.parse(path)
        multi_cols = [("Process", "proc/s"), ("Context", "cswch/s")]
        return add_group_column(df, multi_cols)


class SarBlockLogParser(PerfLogParser):
    @staticmethod
    def regiter_info():
        return LogRegisterInfo(
            log_type="sar (sar -b)", patterns=[r"tps\s+rtps\s+wtps\s+bread/s\s+bwrtn/s"]
        )

    def parse(self, path):
        parser = SarLogParser()
        df = parser.parse(path)
        multi_cols = [
            ("Transaction(/s)", "tps"),
            ("R/W Transaction(/s)", "rtps"),
            ("R/W Transaction(/s)", "wtps"),
            ("Block RW(/s)", "bread/s"),
            ("Block RW(/s)", "bwrtn/s"),
        ]
        return add_group_column(df, multi_cols)


class SarSwapLogParser(PerfLogParser):
    @staticmethod
    def regiter_info():
        return LogRegisterInfo(
            log_type="sar (sar -S)",
            patterns=[r"kbswpfree\s+kbswpused\s+%swpused\s+kbswpcad\s+%swpcad"],
        )

    def parse(self, path):
        parser = SarLogParser()
        df = parser.parse(path)
        multi_cols = [
            ("Swap(KB)", "kbswpfree"),
            ("Swap(KB)", "kbswpused"),
            ("Swap(%)", "%swpused"),
            ("Swapcad(KB)", "kbswpcad"),
            ("Swapcad(%)", "%swpcad"),
        ]
        return add_group_column(df, multi_cols)


class SarRamLogParser(PerfLogParser):
    @staticmethod
    def regiter_info():
        return LogRegisterInfo(
            log_type="sar (sar -r)",
            patterns=[
                r"kbmemfree\s+kbavail\s+kbmemused\s+%memused\s+kbbuffers\s+kbcached\s+kbcommit\s+%commit\s+kbactive\s+kbinact\s+kbdirty"
            ],
        )

    def parse(self, path):
        parser = SarLogParser()
        df = parser.parse(path)
        multi_cols = [
            ("Memory(KB)", "kbmemfree"),
            ("Memory(KB)", "kbavail"),
            ("Memory(KB)", "kbmemused"),
            ("Memory(%)", "%memused"),
            ("Buff/Cache(KB)", "kbbuffers"),
            ("Buff/Cache(KB)", "kbcached"),
            ("Commit(KB)", "kbcommit"),
            ("Commit(%)", "%commit"),
            ("Active(KB)", "kbactive"),
            ("Active(KB)", "kbinact"),
            ("Dirty(KB)", "kbdirty"),
        ]
        return add_group_column(df, multi_cols)


class SarEtcpLogParser(PerfLogParser):
    @staticmethod
    def regiter_info():
        return LogRegisterInfo(
            log_type="sar (sar -n ETCP)",
            patterns=[r"atmptf/s\s+estres/s\s+retrans/s\s+isegerr/s\s+orsts/s"],
        )

    def parse(self, path):
        parser = SarLogParser()
        df = parser.parse(path)
        return df


class SarTcpLogParser(PerfLogParser):
    @staticmethod
    def regiter_info():
        return LogRegisterInfo(
            log_type="sar (sar -n TCP)",
            patterns=[r"active/s\s+passive/s\s+iseg/s\s+oseg/s\s+"],
        )

    def parse(self, path):
        parser = SarLogParser()
        df = parser.parse(path)

        multi_cols = [
            ("AcPs", "active/s"),
            ("AcPs", "passive/s"),
            ("Segment", "iseg/s"),
            ("Segment", "oseg/s"),
        ]
        return add_group_column(df, multi_cols)


# TODO: make it private someway
def add_group_column(df: pd.DataFrame, tuples):
    ifaces = set([iface for iface, _ in df.columns.tolist()])
    multi_cols_with_ifaces = []
    for iface in ifaces:
        for group, col in tuples:
            multi_cols_with_ifaces.append((iface, group, col))
    df.columns = pd.MultiIndex.from_tuples(multi_cols_with_ifaces)
    return df


class SarEdevLogParser(PerfLogParser):
    @staticmethod
    def regiter_info():
        return LogRegisterInfo(
            log_type="sar (sar -n EDEV)",
            patterns=[r"IFACE\s+rxerr/s\s+txerr/s\s+coll/s\s"],
        )

    def parse(self, path):
        parser = SarLogParser()
        df = parser.parse(path)

        multi_cols = [
            ("Error", "rxerr/s"),
            ("Error", "txerr/s"),
            ("Collision", "coll/s"),
            ("Drop", "rxdrop/s"),
            ("Drop", "txdrop/s"),
            ("Carr", "txcarr/s"),
            ("Fram", "rxfram/s"),
            ("FIFO", "rxfifo/s"),
            ("FIFO", "txfifo/s"),
        ]
        return add_group_column(df, multi_cols)


class SarDevLogParser(PerfLogParser):
    @staticmethod
    def regiter_info():
        return LogRegisterInfo(
            log_type="sar (sar -n DEV)",
            patterns=[r"IFACE\s+rxpck/s\s+txpck/s\s+rxkB/s\s+txkB/s"],
        )

    def parse(self, path):
        parser = SarLogParser()
        df = parser.parse(path)

        multi_cols = [
            ("Packet", "rxpck/s"),
            ("Packet", "txpck/s"),
            ("Byte", "rxB/s"),
            ("Byte", "txB/s"),
            ("Compress", "rxcmp/s"),
            ("Compress", "txcmp/s"),
            ("Multicast", "rxmcst/s"),
            ("Usage", "%ifutil"),
        ]
        return add_group_column(df, multi_cols)


class SarCpuLogParser(PerfLogParser):
    @staticmethod
    def regiter_info():
        return LogRegisterInfo(
            log_type="sar (sar -u | -u ALL | -P ALL)",
            patterns=[
                r"CPU\s+\%user\s+\%nice\s+\%system\s+\%iowait\s+\%steal\s+\%idle",
                r"CPU\s+\%usr\s+\%nice\s+\%sys\s+",
            ],
        )

    def parse(self, path):
        parser = SarLogParser()
        df = parser.parse(path)
        return df


class SarLogParser:
    """
    Common sar parser class.
    Used by other sar sub-commands.
    """

    def parse(self, path) -> pd.DataFrame:
        with open(path) as f:
            node_type, cols = self.__parse_header(f)
            df = self.__parse_data(f, node_type, cols)
            return df

    def __parse_data(self, f, node_type, cols) -> pd.DataFrame:
        # TODO: return multi-level-cols-df instead of dictionary
        dataset_dict = collections.OrderedDict()
        for line in f:
            elems = self.__parse_sar_line(line)
            if len(elems) == 0 or (len(elems) > 1 and elems[1] == node_type):
                continue
            if elems[0].endswith(":"):
                continue
            if node_type:
                node = elems[1]
                pos = 2
            else:
                node = "system"
                pos = 1
            nums = [float(e) for e in elems[pos:]]
            data_columns = dataset_dict.setdefault(node, [])
            data_columns.append(nums)

        nodes = dataset_dict.keys()
        dfs = []
        for node in nodes:
            node_cols = [(f"{node_type}:{node}", col) for col in cols]
            df = pd.DataFrame(
                dataset_dict[node], columns=pd.MultiIndex.from_tuples(node_cols)
            )
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


# TODO: check date format
# TODO: check average line
# TODO: unify header line and empty line check process
