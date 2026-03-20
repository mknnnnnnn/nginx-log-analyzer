from .model import NormalizedLog
from typing import Iterator
from datetime import datetime, timedelta


def filters_(logs: Iterator[NormalizedLog], args) -> Iterator[NormalizedLog]:
    filters_ = []

    if args.ip:
        ip = args.ip
        filters_.append(lambda normalized_log: normalized_log.client.ip in ip)

    if args.user:
        user = args.user
        filters_.append(lambda normalized_log: normalized_log.client.user in user)

    if args.method:
        method = args.method
        filters_.append(lambda normalized_log: normalized_log.http.method in method)

    if args.path:
        path = args.path
        filters_.append(
            lambda normalized_log: any(p in normalized_log.http.path for p in path)
        )

    if args.protocol:
        protocol = args.protocol
        filters_.append(lambda normalized_log: protocol == normalized_log.http.protocol)

    if args.status:
        status = args.status
        filters_.append(lambda normalized_log: normalized_log.http.status in status)

    if args.status_range:
        min_, max_ = args.status_range
        filters_.append(
            lambda normalized_log: min_ <= normalized_log.http.status <= max_
        )

    if args.bytes:
        bytes_ = args.bytes
        filters_.append(lambda normalized_log: normalized_log.http.bytes_ == bytes_)

    if args.bytes_range:
        min_, max_ = args.bytes_range
        filters_.append(
            lambda normalized_log: min_ <= normalized_log.http.bytes_ <= max_
        )

    if args.referrer:
        referrer = args.referrer
        filters_.append(
            lambda normalized_log: any(
                normalized_log.referrer != "-" and r in normalized_log.referrer
                for r in referrer
            )
        )

    if args.user_agent:
        user_agent = args.user_agent
        filters_.append(
            lambda normalized_log: any(
                normalized_log.user_agent != "-" and ua in normalized_log.user_agent
                for ua in user_agent
            )
        )

    if args.from_:
        from_ = datetime.fromisoformat(args.from_)
        filters_.append(lambda normalized_log: normalized_log.ts >= from_)

    if args.to:
        to = datetime.fromisoformat(args.to)
        filters_.append(lambda normalized_log: normalized_log.ts <= to)

    if args.last:
        last = args.last
        current = datetime.now()
        diff = current - timedelta(minutes=last)
        filters_.append(lambda normalized_log: diff <= normalized_log.ts <= current)

    for log in logs:
        if all(f(log) for f in filters_):
            yield log
