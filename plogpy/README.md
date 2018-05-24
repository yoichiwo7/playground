> TOOD: The document is under construction. It may contain old/wrong information.


`plogpy` is Python module for generating pandas DataFrame or Excel report file from 
peformance-related logs.
It also provides CLI commands to generate report files.

# Features

- Generates Excel/HTML report from log file.
- Generates pandas DataFrame from log file.
- Option to downsample chart dataset. (Useful for large dataset)
- Prints CSV/JSON.
- Auto detects log type. (Far from smart thongh)

# Supported Input (Log types)

`plogpy` supports log types such as dstat and sar log files.
You can check all supported log types with `list` subcommand.

```bash
# List supported log types.
plogpy-cli list
```

# Supported Output

The following output formats are supported.

  - Excel 2007
    - data sheet, stats sheet, and charts sheet are included.
  - HTML
    - stats tables and line/area charts are included.
  - CSV (Experimental)
  - JSON (Experimental)

# Usage

## Use as Command Line

Generate a report file (Excel2007 format) from a log file. You can also set several options.

```bash
# Generate Excel(2007) -> file/file
plogpy-cli report dstat.log dstat.xlsx

# Generate Excel(2007) -> dir/dir (only current directory)
plogpy-cli report logdir/ reportdir/

# Generate Excel(2007) -> dir/dir (recursively) **Not supported yet**
# plogpy-cli report --recursive logdir/

# Disable chart sheet
plogpy-cli report --no-chart dstat.log dstat.xlsx

# Generate charts for each series
plogpy-cli report --each dstat.log dstat.xlsx

# Generate PNG image charts instead of Excel charts.
plogpy-cli report --png dstat.log dstat.xlsx
```

Generate a HTML report file.

```bash
# Generate HTML report
plogpy-cli html dstat.log dstat.html

# Generate HTML report (downsampling chart samples to 512)
plogpy-cli html --max-samples=512 dstat.log dstat.html
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

# Generate Excel report
plogpy.generate_excel_report("dstat.log" "dstat.xlsx")
```

# TODO: 

Major 

- Manage writer config(ex. chart type) for each logtype.
- Support recursive mode.

Minor 

- Resample option for timestamp index DataFrame.
- Show more information on log type. (ex. regex pattern, expected format example)