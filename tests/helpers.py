"""Shared bits for the tests: the repo root and the build scripts, imported by path."""
import importlib.util
import sys
from pathlib import Path

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent.parent


def load_script(name: str):
    """A scripts/*.py file as a module (their names have dashes, so no plain import)."""
    spec = importlib.util.spec_from_file_location(name.replace("-", "_"), ROOT / "scripts" / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def html_pages() -> list:
    """Every HTML page in the site that has a <head>."""
    return sorted(p for p in ROOT.rglob("*.html")
                  if ".git" not in p.parts and "node_modules" not in p.parts
                  and "<head" in p.read_text(encoding="utf-8"))
