> TOOD: The document is under construction. It may contain old/wrong information.


`plogpy` is CLI/Python module for generating pandas DataFrame or Excel report file from 
peformance-related logs.


# Features

It has following features:

- Generate excel report with data, statistics, and chart sheet.
- Generate pandas DataFrame.
- Output as CSV/JSON.
- Auto detects log type. (Not so smart thongh)
- Provide CLI for generating excel report.

# Supported Input (Log types)

`plogpy` supports log types such as dstat and sar.
You can check all supported log types by following command.

```bash
# List supported log types.
plogpy-cli list
```

# Supported Output

The following output formats are supported.

  - Excel 2007
    - data sheet, stats sheet, and charts sheet are included.
  - CSV (Experimental)
  - JSON (Experimental)

# Usage

## Use as Command Line

Generate a report file (Excel2007 format) from a log file. You can also set several options.

```bash
# Generate Excel(2007) from a log file.
plogpy-cli excel dstat.log dstat.xlsx

# Disable chart sheet
plogpy-cli excel --no-chart dstat.log dstat.xlsx

# Generate charts for each series
plogpy-cli excel --each dstat.log dstat.xlsx

# Generate PNG image charts instead of Excel charts.
plogpy-cli excel --png dstat.log dstat.xlsx
```

See the help for more details.

```bash
# General help
plogpy-cli --help

# Help for target sub command.
plogpy-cli <SUB_COMMAND> --help
```


## Use as Python Module

You can also use plogpy as python module.

Because plogpy uses pandas library under the hood, you can access to DataFrame
and do what ever you need to do.
If you are not satisfied with CLI features, build your own features.

```python
import plogpy

# Generate pandas DataFrame from the specified log
df = plogpy.parse_log("dstat.log")

# Do whatever you need to do with pandas DataFrame
df.head()
df.tail()
df.describe()
```

You can use it for generating files too.

```python
import plogpy

# Generate Excel
plogpy.generate_excel_report("dstat.log" "dstat.xlsx")

# Generate images
plogpy.generate_images("dstat.log" "dstat_images/")
```

# TODO: 

- PNG image charts.
- Resample option for timestamp index DataFrame.
- Nice HTML report with pretty charts.
- Vega/Vega Lite support.
- Show more information on log type. (ex. regex pattern, expected format example)
