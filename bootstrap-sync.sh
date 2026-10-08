#!/usr/bin/env bash
# Copy local edits of home-owned managed files back into this repo's dotfiles.
# Idempotent - safe to re-run. Does not apply anything to home.

set -euo pipefail

MGMT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Harnesses and other tools edit these in place; home is authoritative.
# re-add updates only managed files, leaving new runtime files untracked.
HOME_OWNED_DIRS=(
  "${HOME}/.claude"
  "${HOME}/.codex"
  "${HOME}/.pi"
)

say() { printf "\033[1;34m==>\033[0m %s\n" "$*"; }

say "Syncing managed files from home: ${HOME_OWNED_DIRS[*]}"
chezmoi re-add --source "${MGMT_DIR}/dotfiles" "${HOME_OWNED_DIRS[@]}"
