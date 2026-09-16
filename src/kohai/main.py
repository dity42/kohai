import sys
from kohai.cli.parser import build_parser
from kohai.cli.commands import dispatch

def main() -> None:
    try: 
        parser = build_parser()
        args = parser.parse_args()
    
        if args.command is None:
            parser.print_help()
            return
    
        dispatch(args)
    except KeyboardInterrupt:
        print()
        sys.exit(130)

if __name__ == "__main__":
    main()
