"""CLI entry point for wechat2obsidian."""
import argparse
import os
import sys
import time


def cmd_config(args, cfg):
    """Handle 'config' subcommand."""
    from .config import get_vault_path, save_config

    if args.show:
        print("Current configuration:")
        print("  Vault path: {}".format(cfg.get("vault_path", "(not set)")))
        print("  Attach dir: {}".format(cfg.get("attach_dir", "attachments/wechat")))
        print("  Default folder: {}".format(cfg.get("default_folder", "(none)")))
        print("  Tags: {}".format(", ".join(cfg.get("tags", []))))
        print("  Config file: ~/.wechat2obsidian/config.json")
        return

    # Set vault path
    if args.vault:
        vault = get_vault_path(cfg, args.vault)
        if vault:
            cfg["vault_path"] = vault
            save_config(cfg)
            print("Vault path set: {}".format(vault))
    elif args.attach_dir is not None:
        cfg["attach_dir"] = args.attach_dir
        save_config(cfg)
        print("Attach dir set: {}".format(args.attach_dir))
    elif args.folder is not None:
        cfg["default_folder"] = args.folder
        save_config(cfg)
        print("Default folder set: {}".format(args.folder))
    elif args.reset:
        # Reset config interactively
        print("Resetting configuration...")
        from .config import DEFAULT_CONFIG, CONFIG_DIR, CONFIG_FILE
        import os

        if os.path.exists(CONFIG_FILE):
            os.remove(CONFIG_FILE)
        print("Config reset to defaults.")
    else:
        # Interactive config
        vault = get_vault_path(cfg)
        if vault:
            print("Vault path: {}".format(vault))


def process_one_url(url, cfg, folder=None, attach_arg=None, overwrite=False, vault_arg=None):
    """Process a single WeChat article URL.

    Returns:
        (filepath, error_message) tuple. filepath is None on failure.
    """
    from .fetcher import fetch_article
    from .downloader import extract_image_urls, download_all_images
    from .parser import html_to_markdown, clean_markdown
    from .writer import write_markdown, sanitize_filename
    from .config import get_vault_path, get_attach_dir

    vault_path = get_vault_path(cfg, vault_arg, interactive=True)
    if not vault_path:
        return None, "Vault path not configured. Run: wx2obsidian config"

    attach_dir = get_attach_dir(cfg, attach_arg, vault_path)
    target_folder = folder or cfg.get("default_folder", "")
    tags = cfg.get("tags", ["wechat"])
    delay = cfg.get("request_delay", 0.3)
    timeout = cfg.get("timeout", 30)

    # Step 1: Fetch article
    print("\n[1/4] Fetching: {}".format(url))
    try:
        article = fetch_article(url, timeout=timeout)
    except ValueError as e:
        return None, str(e)
    except Exception as e:
        return None, "Fetch failed: {}".format(str(e))

    print("  Title: {}".format(article.title))
    print("  Author: {}".format(article.author))
    print("  Time: {}".format(article.publish_time))

    # Determine where to save images
    # If attach_dir is None (empty string in config), images go next to the article
    if target_folder:
        article_dir = os.path.join(vault_path, target_folder)
    else:
        article_dir = vault_path
    article_dir = os.path.abspath(article_dir)
    img_save_dir = attach_dir if attach_dir else article_dir

    # Step 2: Download images
    print("\n[2/4] Downloading images...")
    img_urls = extract_image_urls(article.content_soup)
    print("  Found {} image(s)".format(len(img_urls)))

    img_map = {}
    if img_urls and img_save_dir:
        img_map = download_all_images(img_urls, img_save_dir, delay=delay)
        print("  Downloaded: {}/{}".format(len(img_map), len(img_urls)))
    elif img_urls:
        print("  Skipped (no save directory)")

    # Step 3: Convert to Markdown
    print("\n[3/4] Converting to Markdown...")
    body_md = html_to_markdown(article.content_soup, img_map)
    body_md = clean_markdown(body_md)
    print("  Body: {} chars".format(len(body_md)))

    # Step 4: Write file
    print("\n[4/4] Writing to vault...")
    # When images are in same folder, attach_rel is empty (no prefix)
    attach_rel = attach_arg if attach_arg is not None else cfg.get("attach_dir", "attachments/wechat")
    filepath = write_markdown(
        article, body_md, vault_path, target_folder, attach_rel, tags, overwrite
    )
    print("  Saved: {}".format(filepath))

    return filepath, None


def _is_first_run(cfg):
    """Check if this is a first run (no vault path configured)."""
    return not cfg.get("vault_path", "")


def cmd_import(args, cfg):
    """Handle article import (default command)."""
    if args.batch:
        # Batch mode: read URLs from file
        if _is_first_run(cfg) and not getattr(args, "vault", None):
            print("Vault path not configured. Please run setup first:")
            print("  wx2obsidian config")
            print("  wx2obsidian <url> --vault <path>")
            return 1

        urls = []
        with open(args.batch, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                # Skip empty lines and comments
                if line and not line.startswith("#"):
                    urls.append(line)

        if not urls:
            print("No URLs found in: {}".format(args.batch))
            return 1

        print("Batch mode: {} article(s) to process".format(len(urls)))
        errors = []

        for i, url in enumerate(urls, 1):
            print("\n" + "=" * 50)
            print("Article {}/{}".format(i, len(urls)))
            print("=" * 50)
            filepath, err = process_one_url(
                url, cfg, args.folder, args.attach_dir, args.overwrite, getattr(args, "vault", None)
            )
            if err:
                print("  ERROR: {}".format(err))
                errors.append("{}: {}".format(url, err))

            # Delay between articles
            if i < len(urls):
                time.sleep(1)

        # Summary
        print("\n" + "=" * 50)
        print("Batch complete: {}/{} succeeded".format(
            len(urls) - len(errors), len(urls)
        ))
        if errors:
            error_file = "_errors.txt"
            with open(error_file, "w", encoding="utf-8") as f:
                for e in errors:
                    f.write(e + "\n")
            print("Failed URLs saved to: {}".format(error_file))

        return 1 if errors else 0

    else:
        # Single URL mode
        if not args.urls:
            # No URL provided — check if first run
            if _is_first_run(cfg):
                # First-time setup: guide user through configuration
                from .config import get_vault_path
                print()
                vault = get_vault_path(cfg, interactive=True)
                if vault:
                    print("\nSetup complete! Now you can:")
                    print("  wx2obsidian <url>")
                    print("  wx2obsidian --batch links.txt")
                    return 0
                else:
                    print("\nSetup cancelled.")
                    return 1
            else:
                # Already configured, show help
                print("wx2obsidian v0.1.0")
                print("Export WeChat articles to Obsidian-compatible Markdown with images.\n")
                print("Usage:")
                print("  wx2obsidian <url>             Export one article")
                print("  wx2obsidian <url> --folder F  Save to subfolder F")
                print("  wx2obsidian --batch file.txt  Batch export from file")
                print("  wx2obsidian config --show     View current config")
                print("  wx2obsidian config --vault P  Set vault path")
                return 0

        success_count = 0
        for url in args.urls:
            filepath, err = process_one_url(
                url, cfg, args.folder, args.attach_dir, args.overwrite, getattr(args, "vault", None)
            )
            if err:
                print("\nError: {}".format(err))
            else:
                success_count += 1

        return 0 if success_count == len(args.urls) else 1


def main():
    """Main CLI entry point."""
    # Fix Windows console encoding
    if sys.platform == "win32":
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
            sys.stderr.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass

    # Separate URLs from flags before argparse processes them.
    # argparse treats the first positional arg as a subcommand name,
    # so we must extract URLs manually.
    argv = sys.argv[1:]
    config_argv = []
    import_argv = []
    urls = []

    if argv and argv[0] == "config":
        # Everything goes to config subcommand
        config_argv = argv[1:]
        command = "config"
    else:
        command = None
        for arg in argv:
            if arg.startswith("-") or (import_argv and import_argv[-1].startswith("-")):
                import_argv.append(arg)
            else:
                urls.append(arg)

    # Load config
    from .config import load_config
    cfg = load_config()

    if command == "config":
        # Build config sub-parser
        cfg_parser = argparse.ArgumentParser(prog="wx2obsidian config")
        cfg_parser.add_argument("--vault", metavar="PATH", help="Set vault path")
        cfg_parser.add_argument("--attach-dir", metavar="PATH", help="Set attach dir")
        cfg_parser.add_argument("--folder", metavar="NAME", help="Set default folder")
        cfg_parser.add_argument(
            "--show", action="store_true", help="Show current configuration"
        )
        cfg_parser.add_argument(
            "--reset", action="store_true", help="Reset config to defaults"
        )
        args = cfg_parser.parse_args(config_argv)
        return cmd_config(args, cfg)
    else:
        # Build import parser
        parser = argparse.ArgumentParser(
            prog="wx2obsidian",
            description="Export WeChat articles to Obsidian-compatible Markdown with images",
            epilog="Examples:\n"
                   "  wx2obsidian https://mp.weixin.qq.com/s/xxxxx\n"
                   "  wx2obsidian <url> --folder \"My Notes\"\n"
                   "  wx2obsidian --batch links.txt\n"
                   "  wx2obsidian config --vault /path/to/vault\n",
            formatter_class=argparse.RawDescriptionHelpFormatter,
        )
        parser.add_argument(
            "--vault", metavar="PATH",
            help="Obsidian vault path (overrides config)",
        )
        parser.add_argument(
            "--batch", "-b", metavar="FILE",
            help="Read URLs from a text file (one per line)",
        )
        parser.add_argument(
            "--folder", "-f", metavar="NAME",
            help="Subfolder in vault to save articles",
        )
        parser.add_argument(
            "--attach-dir", "-a", metavar="PATH",
            help="Image attachment directory (relative to vault)",
        )
        parser.add_argument(
            "--overwrite", "-o",
            action="store_true",
            help="Overwrite existing files",
        )
        parser.add_argument(
            "--version", "-v",
            action="version",
            version="%(prog)s 0.1.0",
        )
        args = parser.parse_args(import_argv)
        args.urls = urls
        return cmd_import(args, cfg)


if __name__ == "__main__":
    main()
