#!/usr/bin/env bash
# Apply this repo's chezmoi dotfiles.
# Idempotent - safe to re-run.

set -euo pipefail

MGMT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

say() { printf "\033[1;34m==>\033[0m %s\n" "$*"; }

if ! command -v chezmoi >/dev/null 2>&1; then
  if command -v brew >/dev/null 2>&1; then
    say "Installing chezmoi"
    brew install chezmoi
  else
    printf "chezmoi is not installed, and Homebrew is not available.\n" >&2
    printf "Install chezmoi first, then re-run this script.\n" >&2
    exit 1
  fi
fi

CHEZMOI_CFG_DIR="${HOME}/.config/chezmoi"
CHEZMOI_CFG="${CHEZMOI_CFG_DIR}/chezmoi.toml"

mkdir -p "${CHEZMOI_CFG_DIR}"
cat > "${CHEZMOI_CFG}" <<EOF
sourceDir = "${MGMT_DIR}/dotfiles"
EOF

say "Applying chezmoi dotfiles"
chezmoi apply

say "Done. Review any diff with: chezmoi diff"
