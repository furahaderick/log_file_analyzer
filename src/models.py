from dataclasses import dataclass
from datetime import datetime


@dataclass
class RequestLogEntry:
    ip: str
    timestamp: datetime
    method: str
    url: str
    status: int
    bytes: int | None
