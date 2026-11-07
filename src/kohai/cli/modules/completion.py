import shtab

from kohai.app.completion import detect_user_shell, get_completion_paths
from kohai.cli.parser import build_parser


def install_completion() -> None:
    """Generate and install shell completion for the current user's shell."""
    shell = detect_user_shell()
    paths = get_completion_paths()
    comp_file = paths[shell]

    comp_file.parent.mkdir(parents=True, exist_ok=True)
    
    parser = build_parser()
    script = shtab.complete(parser, shell=shell)
    comp_file.write_text(script)

    print(f"Autocomplete for {shell} installed in {comp_file}")
