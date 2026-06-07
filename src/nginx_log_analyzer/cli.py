import argparse

from pathlib import Path

from .reader import Reader
from .clf import CommonLogFormatParser
from .c import CombinedParser
from .filters import filters_
from .stats import top_ip, top_path, bytes_summary
from .report import console_, file_

# from .config import (
#     input_set_path,
#     input_load_path,
#     output_set_path,
#     output_load_path,
# )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--input", type=Path, help="Input path")
    parser.add_argument("-o", "--output", type=Path, help="Output path")

    parser.add_argument(
        "--format",
        dest="format_",
        choices=["c", "clf"],
        help="c stands for combined format and clf stands for common log format",
    )

    # Filters
    parser.add_argument("--ip", nargs="+")
    parser.add_argument("--user", nargs="+")
    parser.add_argument("--method", choices=["GET", "POST", "DELETE"])
    parser.add_argument("--path", nargs="+")
    parser.add_argument("--protocol", nargs="+")
    parser.add_argument("--status", type=int, nargs="+")
    parser.add_argument(
        "--status-range",
        metavar=("min", "max"),
        nargs=2,
        type=int,
    )
    parser.add_argument("--bytes", type=int)
    parser.add_argument(
        "--bytes-range",
        metavar=("min", "max"),
        nargs=2,
        type=int,
    )

    parser.add_argument("--referrer", nargs="+")
    parser.add_argument("--user-agent", nargs="+")
    parser.add_argument("--from", help="In ISO format", dest="from_")
    parser.add_argument("--to", help="In ISO format")
    parser.add_argument(
        "--last",
        help="Last N minutes",
        type=int,
    )

    # Stats
    parser.add_argument(
        "--top-ip",
        metavar="N",
        help="Top N IP addresses",
        type=int,
    )
    parser.add_argument(
        "--top-path",
        metavar="N",
        help="Top N requested paths",
        type=int,
    )
    parser.add_argument(
        "--bytes-summary",
        action="store_true",
        help="Show bytes statistics",
    )

    parser.add_argument(
        "--show", action="store_true", help="Print output to the console"
    )

    return parser


def nginx(log, args):
    if args.format_ == "clf":
        return CommonLogFormatParser().parse_many_lines(log)
    if args.format_ == "c":
        return CombinedParser().parse_many_lines(log)


def stats(log, args):
    if args.top_ip:
        return top_ip(log, args.top_ip)
    if args.top_path:
        return top_path(log, args.top_path)
    if args.bytes_summary:
        return bytes_summary(log)

    return log


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    input_path = args.input

    output_path = args.output

    raw_log = Reader(input_path).load_path()

    normalized_log = nginx(raw_log, args)

    filtered_log = filters_(normalized_log, args)

    stats_log = stats(filtered_log, args)

    file_(stats_log, output_path)

    if args.show:
        console_(output_path)
