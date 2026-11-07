import os
from pathlib import Path

def detect_user_shell() -> str:
    """Detect the current user's shell."""
    shell_path = os.environ.get('SHELL', '/bin/sh')
    shell_name = Path(shell_path).name

    if shell_name == 'zsh':
        return 'zsh'
    elif shell_name == 'fish':
        return 'fish'
    else:
        return 'bash'

def get_completion_paths() -> dict[str, Path]:
    """Return standard paths for shell completion files."""
    home = Path.home()
    return {
        'bash': home / ".local/share/bash-completion/completions/kohai",
        'zsh': home / ".zsh/completions/_kohai",
        'fish': home / ".config/fish/completions/kohai.fish"
    }
