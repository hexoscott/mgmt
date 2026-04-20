# mgmt

Replaces the old nix/home-manager setup. Two tools:

- **Homebrew + Brewfile** — packages (CLI + GUI).
- **chezmoi** — dotfiles in `dotfiles/` (chezmoi source dir, `dot_` prefix = `.` in `$HOME`).

## Fresh machine

```sh
cd ~/mgmt
./bootstrap.sh
```

Installs Homebrew if missing, runs `brew bundle`, writes `~/.config/chezmoi/chezmoi.toml` pointing here, then `chezmoi apply`.

## Day-to-day

```sh
# After editing files in ~/mgmt/dotfiles
chezmoi apply                     # write to $HOME
chezmoi diff                      # preview changes

# After installing new stuff
brew bundle dump --file=Brewfile --force   # refresh Brewfile from current brew state
brew bundle --file=Brewfile                # install anything missing
brew bundle cleanup --file=Brewfile        # list things installed but not in Brewfile
```

## Layout

```
mgmt/
├── Brewfile          # taps, brews, casks
├── bootstrap.sh      # install brew + chezmoi, apply both
└── dotfiles/         # chezmoi source (sourceDir in chezmoi.toml)
    ├── dot_zshrc                   → ~/.zshrc
    ├── dot_tmux.conf               → ~/.tmux.conf
    ├── dot_aerospace.toml          → ~/.aerospace.toml
    ├── dot_zsh/aliases             → ~/.zsh/aliases
    └── dot_config/…                → ~/.config/…
```

## Notes

- `~/.zshrc` still has a line sourcing `~/.nix-profile/bin`; harmless once nix is gone, but you can remove it.
- `solc` in the old `home.nix` became `solidity` in the Brewfile (Homebrew's equivalent formula).
