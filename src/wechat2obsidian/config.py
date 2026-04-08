"""Configuration management for wechat2obsidian."""
import json
import os


CONFIG_DIR = os.path.join(os.path.expanduser("~"), ".wechat2obsidian")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")

DEFAULT_CONFIG = {
    "vault_path": "",
    "attach_dir": "attachments/wechat",
    "default_folder": "",
    "tags": ["wechat"],
    "request_delay": 0.3,
    "timeout": 30,
}


def _ensure_config_dir():
    """Create config directory if it doesn't exist."""
    if not os.path.exists(CONFIG_DIR):
        os.makedirs(CONFIG_DIR)


def load_config():
    """Load config from file, return defaults for missing keys."""
    _ensure_config_dir()
    if not os.path.exists(CONFIG_FILE):
        save_config(DEFAULT_CONFIG)
        return dict(DEFAULT_CONFIG)

    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        cfg = json.load(f)

    # Merge missing default keys
    merged = dict(DEFAULT_CONFIG)
    merged.update(cfg)
    return merged


def save_config(cfg):
    """Save config to file."""
    _ensure_config_dir()
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2, ensure_ascii=False)


def get_vault_path(cfg, vault_arg=None, interactive=True):
    """Get vault path from arg or config.

    Args:
        cfg: config dict
        vault_arg: explicit vault path from CLI --vault
        interactive: if True, prompt user when path is missing (default True)
                     Set False for non-interactive/AI mode.

    Returns:
        vault path string, or None if not set and not interactive.
    """
    if vault_arg:
        return os.path.abspath(vault_arg)

    current = cfg.get("vault_path", "")
    if current and os.path.isdir(current):
        return current
    if current:
        # Path configured but doesn't exist — still return it
        return current

    if not interactive:
        return None

    # Interactive first-time setup
    print("=" * 50)
    print("Welcome to wx2obsidian!")
    print("=" * 50)
    print("First-time setup: please provide your Obsidian vault path.")
    print("This is the root folder of your Obsidian notebook.")
    print()

    path = input("Obsidian vault path: ").strip()
    if not path:
        print("Error: vault path is required.")
        print("You can set it later with: wx2obsidian config --vault <path>")
        return None

    path = os.path.abspath(path)
    if not os.path.isdir(path):
        print("Warning: '{}' does not exist.".format(path))
        confirm = input("Create it? [y/N]: ").strip().lower()
        if confirm == "y":
            os.makedirs(path, exist_ok=True)
        else:
            print("Error: vault path must be a valid directory.")
            return None

    # Also ask about image storage
    print()
    print("Where do you want to save images?")
    print("  1. Same folder as the article (recommended)")
    print("  2. Separate subfolder (e.g. attachments/wechat)")
    print("  3. Keep default (attachments/wechat)")
    choice = input("Choice [1/2/3]: ").strip()

    if choice == "1":
        cfg["attach_dir"] = ""
        print("Images will be saved alongside articles.")
    elif choice == "2":
        custom = input("Subfolder name (relative to vault): ").strip()
        if custom:
            cfg["attach_dir"] = custom
        print("Images will be saved to: {}".format(cfg["attach_dir"]))
    else:
        print("Images will be saved to: {}".format(cfg.get("attach_dir", "attachments/wechat")))

    cfg["vault_path"] = path
    save_config(cfg)
    print("\nConfig saved!")
    print("  Vault: {}".format(path))
    print("  Images: {}".format(cfg.get("attach_dir") or "(same folder as article)"))
    return path


def get_attach_dir(cfg, attach_arg=None, vault_path=None):
    """Get image attachment directory path (absolute).

    If attach_dir is empty string, returns None — meaning images go
    alongside the article file (same folder). Caller should handle this.
    """
    rel_dir = attach_arg if attach_arg is not None else cfg.get("attach_dir", "attachments/wechat")
    # Empty string means "same folder as article"
    if rel_dir == "":
        return None
    if not vault_path:
        return None
    return os.path.join(vault_path, rel_dir)
