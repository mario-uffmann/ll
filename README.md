# ll

A colorized, sorted directory listing for every OS — a single-file Python port
of a PowerShell profile function, so the exact same output (including colors)
works on Windows, Linux and macOS.

## Features

- Directories first, then links, executables and plain files
- Each group sorted by modification time (newest first), then extension
- ANSI colors: directories yellow, executables green, links magenta, hidden dim
- Human-readable sizes (`1.4G`, `23.5M`, locale-aware decimal separator)
- Windows specifics handled: junctions, hidden/system attributes, ANSI enabling
- Standard library only, Python 3.8+

## Install

Clone the repo and add an alias pointing at the launcher for your shell.
The launcher creates a local `.venv` on first run (per machine) and installs
`requirements.txt` into it — no manual setup.

**bash / zsh** (`~/.bashrc` / `~/.zshrc`):

```sh
alias ll='/path/to/ll/ll.sh'
```

**PowerShell** (`$PROFILE`):

```powershell
function ll { & C:\path\to\ll\ll.ps1 @args }
```

**fish** (`~/.config/fish/config.fish`):

```fish
alias ll '/path/to/ll/ll.sh'
```

## Usage

```
ll            # list current directory
ll some/dir   # list another directory
```

## License

[MIT](LICENSE)
