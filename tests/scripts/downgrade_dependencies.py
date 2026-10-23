# Downgrade the dependencies of xdmod-data to the lowest versions that are
# documented as supported by xdmod-data.

import get_config
import subprocess

downgraded_dependencies = [
    x.replace(" >= ", "==") for x in get_config.get_dependencies()
]

subprocess.run(
    "python3 -m pip install --force-reinstall".split() + downgraded_dependencies,
    check=True,
)
