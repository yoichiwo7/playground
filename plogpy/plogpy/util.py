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

# TODO: currently very rough downsampling. make it better.
def down_sample_df(df: pd.DataFrame, max_sample_num=1024, round_num=2) -> pd.DataFrame:
    skip_row_num = 1
    skip_row_num += int(len(df) / max_sample_num)
    s = (df.index.to_series() / skip_row_num).astype(int)
    df = df.groupby(s).std().set_index(s.index[0::skip_row_num])
    if round_num:
        df = df.round(round_num)
    return df