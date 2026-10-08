import sys

import requests
from anime_parsers_ru import errors as api_errors

from kohai.cli.parser import build_parser
from kohai.cli.commands import dispatch
from kohai.exceptions import KohaiError

LIBRARY_ERRORS = (
    api_errors.TokenError,
    api_errors.ServiceError,
    api_errors.PostArgumentsError,
    api_errors.NoResults,
    api_errors.UnexpectedBehavior,
    api_errors.QualityNotFound,
    api_errors.AgeRestricted,
    api_errors.TooManyRequests,
    api_errors.ContentBlocked,
    api_errors.ServiceIsOverloaded,
    api_errors.DecryptionFailure,
    api_errors.Unauthorized,
)

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
    except KohaiError as e:
        print(e)
        sys.exit(1)
    except LIBRARY_ERRORS as e:
        print(f"Error: {e}")
        sys.exit(1)
    except requests.RequestException as e:
        print(f"Network error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
