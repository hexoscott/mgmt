# mgmt

Replaces the old nix/home-manager setup. Three tools:

- **Homebrew + Brewfile** — macOS apps, services, libraries, and system tools.
- **mise + mise.toml** — versioned CLI tools.
- **chezmoi** — dotfiles in `dotfiles/` (chezmoi source dir, `dot_` prefix = `.` in `$HOME`).

## Fresh machine

```sh
cd ~/mgmt
./bootstrap.sh
```

Installs Homebrew and mise if missing, installs both dependency sets, writes `~/.config/chezmoi/chezmoi.toml` pointing here, then runs `chezmoi apply`.

## Day-to-day

```sh
# After editing files in ~/mgmt/dotfiles
chezmoi apply                     # write to $HOME
chezmoi diff                      # preview changes

# After installing new stuff
brew bundle dump --file=Brewfile --force   # refresh Brewfile from current brew state
brew bundle --file=Brewfile                # install anything missing
brew bundle cleanup --file=Brewfile        # list things installed but not in Brewfile
mise use --pin --path ~/mgmt/mise.toml <tool>@<version>
chezmoi apply ~/.mise.toml                   # update the global copy
mise install                                # install pinned CLI versions
```

## devmux

`devmux` is a chezmoi-managed tmux workspace launcher at `~/.local/bin/devmux`.
It creates or reopens a `devmux` tmux session with one window per repo and a
repeatable layout: full-height work pane on the left, agent/run panes stacked
on the right.

```sh
devmux          # open or attach
devmux rebuild  # recreate windows from dotfiles/dot_local/bin/executable_devmux
devmux list     # show configured repos
devmux edit     # edit the launcher config in nvim, or EDITOR if set
./install-devmux.sh  # apply only ~/.tmux.conf and ~/.local/bin/devmux
```

Tmux prefixes are `C-a` and backtick. The old `§` key is also accepted as a
compatibility prefix. Use prefix + `z` to toggle zoom for the active pane; the
active window tab shows `ZOOM` while the current window is zoomed.
Panes use double-line borders with compact headers so each pane reads as a
separate framed workspace.
Tmux extended keys are enabled, and Ghostty maps Shift+Enter to CSI-U modified
Enter so terminal apps can distinguish it from plain Enter.

Edit `dotfiles/dot_local/bin/executable_devmux` to change the repo list or set
optional pane startup commands with `DEVMUX_AGENT_CMD` and `DEVMUX_RUN_CMD`.

## Layout

```
mgmt/
├── Brewfile          # taps, brews, casks
├── mise.toml         # pinned CLI tools
├── bootstrap.sh      # install brew + mise + chezmoi, apply dotfiles
├── install-devmux.sh # apply only tmux + devmux
└── dotfiles/         # chezmoi source (sourceDir in chezmoi.toml)
    ├── dot_zshrc                   → ~/.zshrc
    ├── dot_mise.toml.tmpl          → ~/.mise.toml
    ├── dot_tmux.conf               → ~/.tmux.conf
    ├── dot_local/bin/executable_devmux → ~/.local/bin/devmux
    ├── dot_aerospace.toml          → ~/.aerospace.toml
    ├── dot_zsh/aliases             → ~/.zsh/aliases
    └── dot_config/…                → ~/.config/…
```

## Notes

- `~/.zshrc` still has a line sourcing `~/.nix-profile/bin`; harmless once nix is gone, but you can remove it.
- `solc` in the old `home.nix` became `solidity` in the Brewfile (Homebrew's equivalent formula).
