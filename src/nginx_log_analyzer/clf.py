from dataclasses import dataclass
from typing import Iterator
import re
from datetime import datetime

from .model import Source, Client, HTTP, Request, NormalizedLog


@dataclass
class CommonLogFormatParser:
    _pattern = re.compile(
        r"^(?P<ip>\S+) "
        r"\S+ "
        r"(?P<user>\S+) "
        r"\[(?P<ts>[^\]]+)\] "
        r'"(?P<request>[^"]*)" '
        r"(?P<status>\d{3}) "
        r"(?P<bytes_>\S+)$"
    )

    def parse_line(self, line: str) -> NormalizedLog | None:
        match = self._pattern.match(line)
        if not match:
            return None

        type_ = "nginx"
        format_ = "CLF"

        ip = match.group("ip")
        user = match.group("user")
        ts = match.group("ts")
        ts = datetime.strptime(ts, "%d/%b/%Y:%H:%M:%S %z")
        request = match.group("request")
        status = match.group("status")
        bytes_ = match.group("bytes_")

        if len(request.split()) == 3:
            method, path, protocol = request.split()
        else:
            method, path, protocol = "-", "-", "-"

        status = int(status)
        bytes_ = 0 if bytes_ == "-" else int(bytes_)

        source = Source(type_=type_, format_=format_)
        client = Client(ip=ip, user=user)
        http = HTTP(
            method=method, path=path, protocol=protocol, status=status, bytes_=bytes_
        )
        request = Request(raw=request)

        referrer = "-"
        user_agent = "-"

        return NormalizedLog(
            ts=ts,
            source=source,
            client=client,
            http=http,
            request=request,
            referrer=referrer,
            user_agent=user_agent,
        )

    def parse_many_lines(self, lines: Iterator[str]) -> Iterator[NormalizedLog]:
        for line in lines:
            record = self.parse_line(line)
            if record is not None:
                yield record
