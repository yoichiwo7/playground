def split_csv_line(line, trim_line_sep = True):
    if trim_line_sep:
        line = line.replace("\n", "").replace("\r", "")
    return [s.replace('"', '') for s in line.split(",")]
