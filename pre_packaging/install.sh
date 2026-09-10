#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MIME="$HOME/.local/share/mime/packages"
ICONS="$HOME/.local/share/icons/hicolor/scalable/mimetypes"
APPS="$HOME/.local/share/applications"
mkdir -p "$MIME" "$ICONS" "$APPS"

echo "[1/4] Registering .resy in Linux..."
cp "$ROOT/linux/mime/resy.xml" "$MIME/resy.xml"
cp "$ROOT/linux/icons/application-x-resy.svg" "$ICONS/application-x-resy.svg"
cp "$ROOT/linux/resiris.desktop" "$APPS/resiris.desktop"
command -v update-mime-database >/dev/null 2>&1 && update-mime-database "$HOME/.local/share/mime" >/dev/null || true
command -v update-desktop-database >/dev/null 2>&1 && update-desktop-database "$APPS" >/dev/null 2>&1 || true

echo "[2/4] Setting Resiris as the .resy default application..."
command -v xdg-mime >/dev/null 2>&1 && xdg-mime default resiris.desktop application/x-resy || true

echo "[3/4] Building Seti-based VS Code theme..."
python3 "$ROOT/vscode/build_vsix.py" >/dev/null

echo "[4/4] Installing VS Code extension..."
CODE_CMD=""
for cmd in code code-insiders codium; do
  if command -v "$cmd" >/dev/null 2>&1; then CODE_CMD="$cmd"; break; fi
done
if [[ -n "$CODE_CMD" ]]; then
  "$CODE_CMD" --install-extension "$ROOT/vscode/build/resiris-seti-file-icons-0.1.0.vsix" --force
else
  echo "WARNING: VS Code CLI not found; Linux file-manager integration was still installed."
fi

echo "Done. Restart the file manager if it cached the old icon."
