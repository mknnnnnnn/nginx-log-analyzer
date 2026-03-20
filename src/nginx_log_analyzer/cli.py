import argparse

from pathlib import Path

from .reader import Reader
from .clf import CommonLogFormatParser
from .c import CombinedParser
from .filters import filters_
from .stats import top_ip, top_path, bytes_summary
from .report import console_, file_
from .config import (
    input_set_path,
    input_load_path,
    output_set_path,
    output_load_path,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--set-input-path", type=Path, help="Set the default input path"
    )
    parser.add_argument(
        "--set-output-path", type=Path, help="Set the default output path"
    )

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


def config(args) -> bool:
    new_path = False

    if args.set_input_path:
        input_set_path(args.set_input_path)
        new_path = True

    input_path = input_load_path()

    if input_path is None or not input_path.exists():
        raise ValueError("Input path is not set or does not exist")

    if args.set_output_path:
        output_set_path(args.set_output_path)
        new_path = True

    output_path = output_load_path()

    if output_path is None or not output_path.exists():
        raise ValueError("Output path is not set or does not exist")

    return new_path


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

    if config(args):
        return

    input_path = input_load_path()

    raw_log = Reader(input_path).load_path()

    normalized_log = nginx(raw_log, args)

    filtered_log = filters_(normalized_log, args)

    stats_log = stats(filtered_log, args)

    output_path = output_load_path()

    file_(stats_log, output_path)

    if args.show:
        console_(output_path)
