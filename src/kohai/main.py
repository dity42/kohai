from kohai.cli.parser import build_parser
from kohai.cli.commands import dispatch

def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        return

    dispatch(args)

if __name__ == "__main__":
    main()
