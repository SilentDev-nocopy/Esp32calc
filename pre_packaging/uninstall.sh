#!/usr/bin/env bash
set -euo pipefail

EXTENSION_ID="resiris.resiris-file-icons"

echo "== Resiris VS Code extension uninstaller =="

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
    exit 1
fi

echo "Using: $CODE_CMD"
"$CODE_CMD" --uninstall-extension "$EXTENSION_ID" || true

echo
echo "Removed: Resiris File Icons"
