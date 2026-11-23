"""Command-line interface for base64-cli.

Usage:
    b64 "hello world"                 # encode text -> aGVsbG8gd29ybGQ=
    b64 --decode aGVsbG8gd29ybGQ=     # decode -> hello world
    b64 --urlsafe "hello world"       # URL-safe alphabet
    echo "hello" | b64                # read from stdin
    b64 --decode --wrap 0 file.b64    # decode a file, no line wrapping
"""

import argparse
import sys

from .codec import decode_bytes, encode_bytes, wrap_text


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="b64",
        description="Base64 encode/decode text or files (standard or URL-safe).",
    )
    parser.add_argument(
        "input",
        nargs="?",
        help="text to encode/decode, or a path with --file; reads stdin if omitted",
    )
    parser.add_argument(
        "-d",
        "--decode",
        action="store_true",
        help="decode instead of encode",
    )
    parser.add_argument(
        "-u",
        "--urlsafe",
        action="store_true",
        help="use the URL-safe alphabet (- and _ instead of + and /)",
    )
    parser.add_argument(
        "-f",
        "--file",
        action="store_true",
        help="treat INPUT as a file path instead of literal text",
    )
    parser.add_argument(
        "-w",
        "--wrap",
        type=int,
        default=76,
        metavar="COLS",
        help="wrap encoded output at COLS columns (0 = no wrapping; default 76)",
    )
    parser.add_argument(
        "-o",
        "--output",
        metavar="PATH",
        help="write the result to PATH instead of stdout",
    )
    return parser


def read_input(args: argparse.Namespace) -> bytes:
    if args.input is None:
        return sys.stdin.buffer.read()
    if args.file:
        with open(args.input, "rb") as handle:
            return handle.read()
    return args.input.encode("utf-8")


def run(argv=None) -> int:
    args = build_parser().parse_args(argv)
    try:
        data = read_input(args)
        if args.decode:
            # Decoding works on text: strip whitespace, then decode.
            # The result stays bytes, so binary files round-trip too.
            out = decode_bytes(data.decode("utf-8"), urlsafe=args.urlsafe)
        else:
            out = (wrap_text(encode_bytes(data, urlsafe=args.urlsafe), args.wrap) + "\n").encode("ascii")
    except ValueError as exc:
        print(f"b64: error: {exc}", file=sys.stderr)
        return 2
    except (OSError, UnicodeDecodeError) as exc:
        print(f"b64: error: {exc}", file=sys.stderr)
        return 2

    if args.output:
        with open(args.output, "wb") as handle:
            handle.write(out)
    else:
        sys.stdout.buffer.write(out)
        sys.stdout.buffer.flush()
    return 0


def main() -> None:
    raise SystemExit(run())


if __name__ == "__main__":
    main()
