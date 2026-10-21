import re

log_line_pattern = re.compile(
    r"^(?P<ip>\d{1,3}(?:\.\d{1,3}){3})\s+-\s+-\s+"
    r"\[(?P<timestamp>[^\]]+)\]\s+"
    r'"(?P<method>[A-Z]+)\s+(?P<url>\S+)\s+HTTP/[\d.]+"\s+'
    r"(?P<status>\d{3})\s+(?P<bytes>\d+|-)$"
)

email_pattern = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")

url_pattern = re.compile(r"https?://[^\s<>\"']+")

ip_pattern = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")
