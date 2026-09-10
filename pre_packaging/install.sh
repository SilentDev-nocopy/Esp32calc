#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VSIX="$ROOT/resiris-file-icons-0.1.0.vsix"

echo "== Resiris VS Code extension installer =="

if [[ ! -f "$VSIX" ]]; then
    echo "ERROR: VSIX not found:"
    echo "  $VSIX"
    exit 1
fi

CODE_CMD=""
for cmd in code code-insiders codium; do
    if command -v "$cmd" >/dev/null 2>&1; then
        CODE_CMD="$cmd"
        break
    fi
done

if [[ -z "$CODE_CMD" ]]; then
    echo "ERROR: VS Code CLI not found."
    echo "Expected one of: code, code-insiders, codium"
    echo
    echo "Open VS Code and make sure its 'code' command is available in PATH."
    exit 1
fi

echo "Using: $CODE_CMD"
"$CODE_CMD" --install-extension "$VSIX" --force

echo
echo "Installed: Resiris File Icons"
echo
echo "In VS Code select:"
echo "  Preferences -> File Icon Theme -> Resiris File Icons"
echo
echo "The extension maps *.resy files to the Resy icon."
