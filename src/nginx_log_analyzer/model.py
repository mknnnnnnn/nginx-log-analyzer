from dataclasses import dataclass
from datetime import datetime


@dataclass
class Source:
    type_: str
    format_: str


@dataclass
class Client:
    ip: str
    user: str


@dataclass
class HTTP:
    method: str
    path: str
    protocol: str
    status: int
    bytes_: int


@dataclass
class Request:
    raw: str


@dataclass
class NormalizedLog:
    ts: datetime
    source: Source
    client: Client
    http: HTTP
    request: Request
    referrer: str
    user_agent: str

    def to_dict(self):
        return {
            "ts": self.ts.isoformat(),
            "source": {"type": self.source.type_, "format": self.source.format_},
            "clent": {"ip": self.client.ip, "user": self.client.user},
            "http": {
                "method": self.http.method,
                "path": self.http.path,
                "protocol": self.http.protocol,
                "status": self.http.status,
                "bytes": self.http.bytes_,
            },
            "request": {"raw": self.request.raw},
            "referrer": self.referrer,
            "user_agent": self.user_agent,
        }
