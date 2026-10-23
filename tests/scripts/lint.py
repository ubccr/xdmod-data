# Run Black and Flake8 linters.

from pathlib import Path
import subprocess

scripts_dir = Path(__file__).resolve().parent
project_dir = scripts_dir / ".." / ".."

print("Formatting with Black...")
subprocess.run(
    f"python3 {scripts_dir}/format.py --check".split(),
    check=True,
)

print("Linting with Flake8...")
subprocess.run(
    f"python3 -m flake8 --select C90,F401,F841 --max-complexity 10 --exclude __init__.py {project_dir}".split(),
    check=True,
)
print("Linting successful")
