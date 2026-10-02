"""Run with python3 test-bootstrap-chezmoi.py (requires chezmoi)."""

import os
from pathlib import Path
import shutil
import subprocess
import tempfile


with tempfile.TemporaryDirectory() as temporary:
    root = Path(temporary)
    repo, home = root / "repo", root / "home"
    repo.mkdir()
    home.mkdir()
    script = repo / "bootstrap-chezmoi.sh"
    shutil.copyfile(Path(__file__).with_name(script.name), script)
    source = repo / "dotfiles"
    files = {
        ".claude/settings.json": "{}\n",
        ".claude/CLAUDE.md": "Instructions\n",
        ".claude/skills/example/SKILL.md": "Claude skill\n",
        ".codex/config.toml": "# repo\n",
        ".codex/skills/example/SKILL.md": "Codex skill\n",
        ".pi/agent/settings.json": "{}\n",
        ".pi/agent/models.json": "{}\n",
        ".pi/agent/extensions/example/index.ts": "// Pi extension\n",
    }
    for name, content in files.items():
        path = source / name.replace(".", "dot_", 1)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
    (source / "dot_unrelated").write_text("repo-owned\n")
    env = {**os.environ, "HOME": str(home), "XDG_CONFIG_HOME": str(home / ".config"),
           "XDG_CACHE_HOME": str(home / ".cache"), "XDG_DATA_HOME": str(home / ".local/share")}

    def run():
        subprocess.run(["bash", str(script)], env=env, check=True, capture_output=True)

    run()  # Fresh machine: missing directories and files are installed.
    for name, content in files.items():
        assert (home / name).read_text() == content
        (home / name).write_text(content + "\n")
    (home / ".claude/auth.json").write_text("unmanaged\n")
    (home / ".codex/sessions").mkdir()
    (home / ".codex/sessions/session.json").write_text("unmanaged\n")
    (home / ".pi/agent/auth.json").write_text("unmanaged\n")
    (home / ".pi/agent/sessions").mkdir()
    (home / ".pi/agent/sessions/session.json").write_text("unmanaged\n")
    (source / "dot_unrelated").write_text("updated repo-owned\n")
    run()  # Home edits win, while unrelated dotfiles still apply normally.
    run()  # Repeat runs are safe.
    for name, content in files.items():
        assert (source / name.replace(".", "dot_", 1)).read_text() == content + "\n"
        assert (home / name).read_text() == content + "\n"
    assert not (source / "dot_claude/auth.json").exists()
    assert not (source / "dot_codex/sessions").exists()
    assert not (source / "dot_pi/agent/auth.json").exists()
    assert not (source / "dot_pi/agent/sessions").exists()
    assert (home / ".unrelated").read_text() == "updated repo-owned\n"
    print("PASS: fresh install, configs, instructions, skills, repeat runs, unmanaged files")
