"""PyInstaller entry point for wechat2obsidian.

This file avoids the relative import issue by importing the package
as an absolute import after PyInstaller sets up the path.
"""
import sys
import os

# Ensure the package is importable (PyInstaller handles this for --onefile,
# but we also support running this script directly during development)
if __name__ == "__main__":
    # When running as a script (not frozen), add src/ to path
    if not getattr(sys, "frozen", False):
        src_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "src")
        if src_dir not in sys.path:
            sys.path.insert(0, src_dir)

    from wechat2obsidian.cli import main
    exit_code = main()

    # When running as a frozen exe, prevent the window from closing immediately
    if getattr(sys, "frozen", False):
        print()
        input("Press Enter to exit...")

    sys.exit(exit_code if exit_code is not None else 0)
