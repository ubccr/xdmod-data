from pathlib import Path
import shutil

project_dir = Path(__file__).resolve().parent.parent.parent

for pycache_dir in project_dir.rglob("__pycache__"):
    if pycache_dir.is_dir():
        shutil.rmtree(pycache_dir)

for file in (project_dir / "tests" / "scratch").iterdir():
    if file.is_file():
        file.unlink()
