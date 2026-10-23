# Format using Black.
# Run with --check to check if formatting needs to be applied.

import get_config
from pathlib import Path
import subprocess
import sys

check = ""
if len(sys.argv) > 1 and sys.argv[1] == "--check":
    check = "--check"

target_version = "py" + str(get_config.get_max_python_version()).replace(".", "")
project_dir = Path(__file__).resolve().parent.parent.parent

subprocess.run(
    f"python3 -m black {check} --target-version={target_version} {project_dir}".split(),
    check=True,
)
