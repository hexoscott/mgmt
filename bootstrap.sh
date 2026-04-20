#!/usr/bin/env bash
# Bootstrap a fresh Mac: Homebrew + Brewfile + chezmoi apply.
# Idempotent — safe to re-run.

set -euo pipefail

MGMT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

say() { printf "\033[1;34m==>\033[0m %s\n" "$*"; }

# 1. Homebrew
if ! command -v brew >/dev/null 2>&1; then
  say "Installing Homebrew"
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi

# Make brew available in this shell on Apple Silicon / Intel
if [[ -x /opt/homebrew/bin/brew ]]; then
  eval "$(/opt/homebrew/bin/brew shellenv)"
elif [[ -x /usr/local/bin/brew ]]; then
  eval "$(/usr/local/bin/brew shellenv)"
fi

# 2. Brew bundle
say "Installing packages from Brewfile"
brew bundle --file="${MGMT_DIR}/Brewfile"

# 3. chezmoi (brew bundle installs it, but double-check)
if ! command -v chezmoi >/dev/null 2>&1; then
  say "Installing chezmoi"
  brew install chezmoi
fi

# 4. Point chezmoi at this repo's dotfiles and apply
CHEZMOI_CFG_DIR="${HOME}/.config/chezmoi"
CHEZMOI_CFG="${CHEZMOI_CFG_DIR}/chezmoi.toml"
mkdir -p "${CHEZMOI_CFG_DIR}"
cat > "${CHEZMOI_CFG}" <<EOF
sourceDir = "${MGMT_DIR}/dotfiles"
EOF

say "Applying chezmoi dotfiles"
chezmoi apply

say "Done. Review any diff with: chezmoi diff"
