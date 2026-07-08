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

Clone the repo and run the installer — it adds the `ll` alias to your shell
config (idempotent) and pre-creates the local `.venv`:

**Linux / macOS** (bash, zsh, fish):

```sh
git clone https://github.com/mario-uffmann/ll ~/ll
~/ll/install.sh
```

**Windows** (PowerShell):

```powershell
git clone https://github.com/mario-uffmann/ll C:\tools\ll
C:\tools\ll\install.ps1
```

Open a new shell afterwards. Prefer manual setup? Point an alias at
`ll.sh` / `ll.ps1` yourself — the launcher creates the `.venv` on first run.

## Usage

```
ll            # list current directory
ll some/dir   # list another directory
```

## License

[MIT](LICENSE)
