#!/usr/bin/env sh
# Installs the ll alias into the user's shell config and pre-creates the venv.
# Idempotent: running it again changes nothing.
set -e

REPO="$(cd "$(dirname "$0")" && pwd)"

case "${SHELL:-}" in
    */zsh)  RC="$HOME/.zshrc";  ALIAS_LINE="alias ll='$REPO/ll.sh'" ;;
    */fish) RC="$HOME/.config/fish/config.fish"; ALIAS_LINE="alias ll '$REPO/ll.sh'" ;;
    *)      RC="$HOME/.bashrc"; ALIAS_LINE="alias ll='$REPO/ll.sh'" ;;
esac

mkdir -p "$(dirname "$RC")"
touch "$RC"

if grep -Fq "$REPO/ll.sh" "$RC"; then
    echo "ll alias already present in $RC"
else
    printf '\n# ll (https://github.com/mario-uffmann/ll)\n%s\n' "$ALIAS_LINE" >> "$RC"
    echo "ll alias added to $RC"
fi

"$REPO/ll.sh" "$REPO" >/dev/null
echo "venv ready - open a new shell and run: ll"
