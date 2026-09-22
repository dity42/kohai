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
        # exit code 130 = 128 + SIGINT, standard for "interrupted by user"
        print() # newline after ^C so shell prompt doesn't stick
        sys.exit(130)

if __name__ == "__main__":
    main()
