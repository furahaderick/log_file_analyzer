# flake8: noqa

import re

log_line_pattern = re.compile(
    r"^(?P<ip>\d{1,3}(?:\.\d{1,3}){3})\s+-\s+-\s+"  # ip eg. 192.168.0.1
    r"\[(?P<timestamp>[^\]]+)\]\s+"  # timestamp eg. [21/Oct/2026:12:50:00 +0200]
    r'"(?P<method>[A-Z]+)\s+(?P<url>\S+)\s+HTTP/[\d.]+"\s+'  # method & url eg. GET /index.html
    r"(?P<status>\d{3})\s+(?P<bytes>\d+|-)$"  # status & bytes eg. 200 512
)

email_pattern = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")
