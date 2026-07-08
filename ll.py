#!/usr/bin/env python3
"""ll - a colorized, sorted directory listing.

Cross-platform port of a PowerShell profile function. Directories first,
then links, executables and plain files, each group sorted by modification
time (newest first). Colors are plain ANSI escape codes so the output looks
identical in any modern terminal on Windows, Linux and macOS.

Requires Python 3.8+, standard library only.
"""

import argparse
import locale
import os
import stat
import sys
from datetime import datetime

ESC = "\x1b"
RESET = f"{ESC}[0m"

COLORS = {
    "path": f"{ESC}[1;36m",  # bold cyan
    "header": f"{ESC}[2;37m",  # dim grey
    "dir": f"{ESC}[1;33m",  # bold yellow
    "exe": f"{ESC}[1;32m",  # bold green
    "link": f"{ESC}[1;35m",  # bold magenta
    "hidden": f"{ESC}[2;37m",  # dim grey
    "file": f"{ESC}[0;37m",  # white
    "size": f"{ESC}[0;33m",  # yellow
    "date": f"{ESC}[0;36m",  # cyan
}

EXE_EXTENSIONS = {".exe", ".bat", ".cmd", ".ps1", ".psm1", ".sh"}

IS_WINDOWS = os.name == "nt"
MODE_WIDTH = 5 if IS_WINDOWS else 10


def enable_ansi_on_windows() -> None:
    if not IS_WINDOWS:
        return
    import ctypes

    kernel32 = ctypes.windll.kernel32
    handle = kernel32.GetStdHandle(-11)  # STD_OUTPUT_HANDLE
    mode = ctypes.c_uint32()
    if kernel32.GetConsoleMode(handle, ctypes.byref(mode)):
        ENABLE_VIRTUAL_TERMINAL_PROCESSING = 0x0004
        kernel32.SetConsoleMode(handle, mode.value | ENABLE_VIRTUAL_TERMINAL_PROCESSING)


class Entry:
    def __init__(self, dir_entry: os.DirEntry):
        self.name = dir_entry.name
        self.path = dir_entry.path
        st = dir_entry.stat(follow_symlinks=False)
        self.mtime = st.st_mtime
        self.size = st.st_size
        self.link_target = self._read_link_target(dir_entry, st)
        self.is_link = self.link_target is not None
        self.is_dir = dir_entry.is_dir(follow_symlinks=False) or (
            self.is_link and dir_entry.is_dir(follow_symlinks=True)
        )
        self.is_hidden = self._detect_hidden(st)
        self.extension = os.path.splitext(self.name)[1].lower()
        self.is_exe = self._detect_exe(st)
        self.mode = self._format_mode(st)

    @staticmethod
    def _read_link_target(dir_entry: os.DirEntry, st: os.stat_result):
        """Return the link target, or None if the entry is not a link.

        On Windows, symlinks and junctions resolve via readlink; other reparse
        points (e.g. OneDrive cloud folders) fail and are treated as regular
        entries.
        """
        attrs = getattr(st, "st_file_attributes", 0)
        may_be_link = dir_entry.is_symlink() or (
            IS_WINDOWS and attrs & stat.FILE_ATTRIBUTE_REPARSE_POINT
        )
        if not may_be_link:
            return None
        try:
            target = os.readlink(dir_entry.path)
        except OSError:
            return "?" if dir_entry.is_symlink() else None
        if target.startswith("\\\\?\\"):
            target = target[4:]
        return target

    def _detect_hidden(self, st: os.stat_result) -> bool:
        if IS_WINDOWS:
            attrs = getattr(st, "st_file_attributes", 0)
            return bool(attrs & stat.FILE_ATTRIBUTE_HIDDEN)
        return self.name.startswith(".")

    def _detect_exe(self, st: os.stat_result) -> bool:
        if self.is_dir:
            return False
        if self.extension in EXE_EXTENSIONS:
            return True
        if not IS_WINDOWS:
            return bool(st.st_mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH))
        return False

    def _format_mode(self, st: os.stat_result) -> str:
        if not IS_WINDOWS:
            return stat.filemode(st.st_mode)
        attrs = getattr(st, "st_file_attributes", 0)
        flags = [
            "l" if self.is_link else ("d" if self.is_dir else "-"),
            "a" if attrs & stat.FILE_ATTRIBUTE_ARCHIVE else "-",
            "r" if attrs & stat.FILE_ATTRIBUTE_READONLY else "-",
            "h" if attrs & stat.FILE_ATTRIBUTE_HIDDEN else "-",
            "s" if attrs & stat.FILE_ATTRIBUTE_SYSTEM else "-",
        ]
        return "".join(flags)

    @property
    def sort_category(self) -> int:
        if self.is_link:
            return 1
        if self.is_dir:
            return 0
        if self.extension in EXE_EXTENSIONS:
            return 2
        return 3

    @property
    def color(self) -> str:
        if self.is_link:
            return COLORS["link"]
        if self.is_dir:
            return COLORS["dir"]
        if self.is_hidden:
            return COLORS["hidden"]
        if self.is_exe:
            return COLORS["exe"]
        return COLORS["file"]

    @property
    def display_name(self) -> str:
        name = self.name + os.sep if self.is_dir and not self.is_link else self.name
        if self.is_link:
            name += f" -> {self.link_target}"
        return name


def format_size(num_bytes: int) -> str:
    for factor, unit in ((1024**3, "G"), (1024**2, "M"), (1024, "K")):
        if num_bytes >= factor:
            return locale.format_string("%.1f", num_bytes / factor) + unit
    return f"{num_bytes}B"


def list_entries(path: str) -> list:
    with os.scandir(path) as it:
        entries = [Entry(e) for e in it]
    entries.sort(key=lambda e: (e.sort_category, -e.mtime, e.extension))
    return entries


def render(path: str, entries: list) -> None:
    c = COLORS
    print()
    print(f"  {c['path']}{path}{RESET}")
    print(f"  {c['header']}{'-' * (len(path) + 2)}{RESET}")
    header = f"  {'Mode':<{MODE_WIDTH}} {'Size':>10}  {'Modified':<19}  Name"
    print(f"{c['header']}{header}{RESET}")
    print()
    for e in entries:
        size = "<DIR>" if e.is_dir else format_size(e.size)
        date = datetime.fromtimestamp(e.mtime).strftime("%Y-%m-%d %H:%M")
        print(
            f"  {e.mode:<{MODE_WIDTH}} "
            f"{c['size']}{size:>10}{RESET}  "
            f"{c['date']}{date}{RESET}  "
            f"{e.color}{e.display_name}{RESET}"
        )
    print()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("path", nargs="?", default=".", help="directory to list (default: .)")
    args = parser.parse_args()

    locale.setlocale(locale.LC_ALL, "")
    enable_ansi_on_windows()

    resolved = os.path.abspath(args.path)
    if not os.path.isdir(resolved):
        print(f"ll: not a directory: {args.path}", file=sys.stderr)
        return 1

    render(resolved, list_entries(resolved))
    return 0


if __name__ == "__main__":
    sys.exit(main())
