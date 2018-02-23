## Supported Log

- dstat
- vmstat
- sar
- iostat


## Usage

```python
import plogpy

logdata = plogpy.parse(logfile, type=plogpy.TYPE.DSTAT)

logdata["cpu"]["all"] 
# -> {"usr": [...]}

logdata["cpu"]["cpu0"] 
# -> {"usr": [...]}

logdata = plogpy.parse_as_stream(logfile, "cpu/cpu0", type=plogpy.TYPE.DSTAT)
logdata.title()
# -> "CPU Usage"
logdata.node()
# -> "cpu0"
logdata.headers()
# -> ["usr", "sys", "wa"]
logdata.next()
# -> [42.8, 7.0, 10.5]

inspected_info = plogpy.inspect(logfile)
inspected_info.type() 
# -> TYPE.DSTAT
inspected_info.categories() 
# -> ["cpu", "memory", "xxx", ...]
inspected_info.nodes("cpu") 
# -> ["all", "cpu0", "cpu1"]


"""
{
    // PerfLogData
    "cpu_usage": {
        "all": {
            // PerfDataset
            "usr": [...],
            "sys": [...],
        },
        "cpu0": {
            "usr": [...],
            "sys": [...],
        },
    },
    "memory": {
        "": {
            "used": [...],
            "free": [...],
            "cached": [...],
            "buff": [...],
        }
    }
}
"""
```