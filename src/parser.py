from datetime import datetime

from src.models import RequestLogEntry
from src.patterns import log_line_pattern


def parse_log_line(line: str) -> RequestLogEntry | None:
    match = log_line_pattern.match(line)

    if not match:
        return None

    ip = match.group("ip")

    timestamp_str = match.group("timestamp")
    timestamp = datetime.strptime(timestamp_str, "%d/%b/%Y:%H:%M:%S %z")

    method = match.group("method")
    url = match.group("url")
    status = int(match.group("status"))
    byte_count = int(match.group("bytes")) if match.group("bytes") != "-" else None

    request_log_entry = RequestLogEntry(
        ip=ip,
        timestamp=timestamp,
        method=method,
        url=url,
        status=status,
        bytes=byte_count,
    )

    return request_log_entry
