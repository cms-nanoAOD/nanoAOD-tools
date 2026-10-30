"""Command-line interface to correctionlib

"""
import argparse
import sys
from typing import Any

from rich.console import Console

import correctionlib.version
from correctionlib.highlevel import model_auto, open_auto


def validate(console: Console, args: argparse.Namespace) -> int:
    """Check if all files are valid"""
    retcode = 0
    for file in args.files:
        try:
            if not args.quiet:
                console.rule(f"[blue]Validating file {file}")
            cset = model_auto(open_auto(file))
            if args.version and cset.schema_version != args.version:
                raise ValueError(
                    f"Schema version {cset.schema_version} does not match the required version {args.version}"
                )
        except Exception as ex:
            if not args.quiet:
                console.print(str(ex))
            retcode = 1
            if args.failfast:
                break
        else:
            if not args.quiet:
                console.print("[green]All OK :heavy_check_mark:")
    return retcode


def setup_validate(subparsers: Any) -> None:
    parser = subparsers.add_parser("validate", help=validate.__doc__)
    parser.set_defaults(command=validate)
    parser.add_argument(
        "--quiet",
        "-q",
        action="store_true",
        help="Suppress error printout, only produce a returncode",
    )
    parser.add_argument(
        "--failfast",
        "-f",
        action="store_true",
        help="Fail on first invalid file",
    )
    parser.add_argument(
        "--version",
        "-v",
        type=int,
        default=None,
        help="Validate against specific schema version",
    )
    parser.add_argument("files", nargs="+", metavar="FILE")


def summary(console: Console, args: argparse.Namespace) -> int:
    for file in args.files:
        console.rule(f"[blue]Corrections in file {file}")
        cset = model_auto(open_auto(file))
        console.print(cset)
    return 0


def setup_summary(subparsers: Any) -> None:
    parser = subparsers.add_parser(
        "summary", help="Print a summmary of the corrections"
    )
    parser.set_defaults(command=summary)
    parser.add_argument("files", nargs="+", metavar="FILE")


def merge(console: Console, args: argparse.Namespace) -> int:
    cset = model_auto(open_auto(args.files[0]))
    for file in args.files[1:]:
        cset2 = model_auto(open_auto(file))
        if cset2.schema_version != cset.schema_version:
            console.print("[red]Mixed schema versions detected")
            return 1
        for corr2 in cset2.corrections:
            if any(corr.name == corr2.name for corr in cset.corrections):
                console.print(
                    f"[red]Correction '{corr2.name}' from {file} is a duplicate"
                )
                return 1
            cset.corrections.append(corr2)
        for corr2 in cset2.compound_corrections if cset2.compound_corrections else []:
            if cset.compound_corrections is None:
                cset.compound_corrections = []
            if any(corr.name == corr2.name for corr in cset.compound_corrections):
                console.print(
                    f"[red]Compound correction '{corr2.name}' from {file} is a duplicate"
                )
                return 1
            cset.compound_corrections.append(corr2)
    cset.description = "Merged from " + " ".join(args.files)
    if args.format == "compact":
        sys.stdout.write(cset.json())
    elif args.format == "indented":
        sys.stdout.write(cset.json(indent=4) + "\n")
    elif args.format == "pretty":
        from correctionlib.JSONEncoder import dumps

        sys.stdout.write(dumps(cset) + "\n")
    else:
        return 1
    return 0


def setup_merge(subparsers: Any) -> None:
    parser = subparsers.add_parser(
        "merge", help="Merge one or more correction files and print to stdout"
    )
    parser.set_defaults(command=merge)
    parser.add_argument(
        "-f",
        "--format",
        type=str,
        help="JSON output formatting (default: %(default)s)",
        choices=("compact", "indented", "pretty"),
        default="compact",
    )
    parser.add_argument("files", nargs="+", metavar="FILE")


def config(console: Console, args: argparse.Namespace) -> int:
    import pkg_resources

    incdir = pkg_resources.resource_filename("correctionlib", "include")
    libdir = pkg_resources.resource_filename("correctionlib", "lib")
    out = []
    if args.version:
        out.append(correctionlib.version.version)
    if args.incdir:
        out.append(incdir)
    if args.cflags:
        out.append(f"-std=c++17 -I{incdir}")
    if args.libdir:
        out.append(libdir)
    if args.ldflags:
        out.append(f"-L{libdir} -lcorrectionlib")
    if args.rpath:
        out.append(f"-Wl,-rpath,{libdir}")
    if args.cmake:
        out.append(
            f"-Dcorrectionlib_DIR={pkg_resources.resource_filename('correctionlib', 'cmake')}"
        )
    console.out(" ".join(out), highlight=False)
    return 0


def setup_config(subparsers: Any) -> None:
    parser = subparsers.add_parser(
        "config", help="Configuration and linking information"
    )
    parser.set_defaults(command=config)
    parser.add_argument("-v", "--version", action="store_true")
    parser.add_argument("--incdir", action="store_true")
    parser.add_argument("--cflags", action="store_true")
    parser.add_argument("--libdir", action="store_true")
    parser.add_argument("--ldflags", action="store_true")
    parser.add_argument(
        "--rpath", action="store_true", help="Include library path hint in linker"
    )
    parser.add_argument("--cmake", action="store_true", help="CMake dependency flags")


def main() -> int:
    parser = argparse.ArgumentParser(prog="correction", description=__doc__)
    parser.add_argument(
        "--width",
        type=int,
        default=100,
        help="Rich output width",
    )
    parser.add_argument("--html", type=str, help="Save terminal output to an HTML file")
    subparsers = parser.add_subparsers()
    setup_validate(subparsers)
    setup_summary(subparsers)
    setup_merge(subparsers)
    setup_config(subparsers)
    args = parser.parse_args()

    console = Console(width=args.width, record=bool(args.html))
    # py3.7: subparsers has required=True option
    if hasattr(args, "command"):
        retcode: int = args.command(console, args)
        if args.html:
            console.save_html(args.html)
        return retcode

    parser.parse_args(["-h"])
    return 0


if __name__ == "__main__":
    exit(main())
