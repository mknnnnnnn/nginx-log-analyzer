from .model import NormalizedLog
from typing import Iterator


def top_ip(logs: Iterator[NormalizedLog], args) -> list[tuple[str, int]]:
    top_ip = {}
    n = args.top_ip

    for log in logs:
        ip = log.client.ip
        top_ip[ip] = top_ip.get(ip, 0) + 1

    sorted_top_ip = sorted(top_ip.items(), key=lambda item: item[1], reverse=True)

    return sorted_top_ip[:n]


def top_path(logs: Iterator[NormalizedLog], args) -> list[tuple[str, int]]:
    top_path = {}
    n = args.top_path

    for log in logs:
        path = log.http.path
        top_path[path] = top_path.get(path, 0) + 1

    sorted_top_path = sorted(top_path.items(), key=lambda item: item[1], reverse=True)

    return sorted_top_path[:n]


def bytes_summary(logs: Iterator[NormalizedLog]) -> dict:
    sum_ = 0
    min_ = None
    max_ = None
    count = 0
    for log in logs:
        count += 1
        sum_ += log.http.bytes_

        if min_ is None or log.http.bytes_ < min_:
            min_ = log.http.bytes_

        if max_ is None or log.http.bytes_ > max_:
            max_ = log.http.bytes_

    avarage = sum_ / count if count != 0 else 0

    return {"sum": sum_, "min": min_, "max": max_, "avarage": avarage, "count": count}
