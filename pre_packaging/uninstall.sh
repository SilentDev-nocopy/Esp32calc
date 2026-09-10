#!/usr/bin/env bash
set -euo pipefail
MIME="$HOME/.local/share/mime/packages"
ICONS="$HOME/.local/share/icons/hicolor/scalable/mimetypes"
APPS="$HOME/.local/share/applications"

for cmd in code code-insiders codium; do
  if command -v "$cmd" >/dev/null 2>&1; then
    "$cmd" --uninstall-extension resiris.resiris-seti-file-icons >/dev/null 2>&1 || true
  fi
done
rm -f "$MIME/resy.xml" "$ICONS/application-x-resy.svg" "$APPS/resiris.desktop"
command -v update-mime-database >/dev/null 2>&1 && update-mime-database "$HOME/.local/share/mime" >/dev/null 2>&1 || true
command -v update-desktop-database >/dev/null 2>&1 && update-desktop-database "$APPS" >/dev/null 2>&1 || true
echo "Resiris Linux file integration and VS Code extension removed."
