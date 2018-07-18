from enum import Enum


class LogType(Enum):
    AUTO_DETECTION = "#Auto Detection#"

    DSTAT = "dstat"
    SAR_CPU = "sar -u"
    SAR_CPU_ALL = "sar -P ALL, sar -u ALL"
