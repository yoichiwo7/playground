TOOD: The document is under construction. It may contain old/wrong information.

# Overview 

`plogpy` is CLI/Python module for generating a report from a performance-related log file.

It has following features:

- Generate excel report with data, statistics, and chart sheet.
- Generate pandas DataFrame.
- Output as CSV/JSON.
- Auto detects log type. (Not so smart thongh)

TODO: 

- Plugin to extend supported log type.
  - If you can generate DataFrame, you've completed the plugin.
- PNG image charts.
- Resample to reduce large data.
- Nice HTML report with pretty charts.
- Vega/Vega Lite support.


# Supported Output

The following output formats are supported.

  - Excel
  - CSV (Experimental)
  - JSON (Experimental)


# Supported log types

Current version support following type of performance-related log file.

  - dstat (--output)
  - sar

TODO:

  - ~~vmstat~~
  - ~~meminfo~~
  - ~~docker stats~~
  - ~~df~~
  - ~~xxx~~


# CLI Usage

```bash
# Generate Excel(2007) from a log file.
plogpy-cli excel dstat.log dstat.xlsx

# Disable chart sheet
plogpy-cli excel --no-chart dstat.log dstat.xlsx

# Charts for each series
plogpy-cli excel --each dstat.log dstat.xlsx

# PNG image charts
plogpy-cli excel --png dstat.log dstat.xlsx
```

See the help for more details.

```bash
# General help
plogpy-cli --help

# Help for target sub command.
plogpy-cli <SUB_COMMAND> --help
```


# Module Usage

You can also use plogpy as python module.
Because plogpy uses pandas library under the hood, you can access to DataFrame
and do what ever you need to do.

```python
import plogpy

# Generate pandas DataFrame from the specified log
df = plogpy.parse_log("dstat.log")

# Specify log type
df = plogpy.parse_log("dstat.log", LogType.DSTAT)

# Generate Excel from specfied log
df = plogpy.generate_excel_report("dstat.log" "dstat.xlsx")
```