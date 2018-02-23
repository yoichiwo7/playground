import collections

import pandas as pd


def split_csv_line(line, trim_line_sep = True):
    if trim_line_sep:
        line = line.replace("\n", "").replace("\r", "")
    return [s.replace('"', '') for s in line.split(",")]


def get_parent_leaf_headers(df: pd.DataFrame) -> list:
    """
    Returns ordered dictionary. (key=parents_tuple, value=leaf_cols)
    """
    #TODO: get leaf headers and parents -> {("cpu usage") : ["usr", "sys", ...]}
    collected_headers = collections.OrderedDict()
    is_multi = isinstance(df.keys(), pd.core.indexes.multi.MultiIndex)
    if is_multi:
        # Multi level
        for hdrs in df.keys():
            parents = hdrs[0:-1]
            leaf = hdrs[-1]
            v = collected_headers.setdefault(parents, [])
            v.append(leaf)
        return collected_headers
    else:
        # Single level
        for hdr in df.keys():
            leaf = hdr
            v = collected_headers.setdefault((), [])
            v.append(leaf)
        return collected_headers