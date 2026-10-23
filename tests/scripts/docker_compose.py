# Set up a Docker Compose application stack for local testing.

import get_config
from pathlib import Path
import subprocess
import sys

# Make sure either 'up' or 'down' was specified.
if len(sys.argv) == 2 and sys.argv[1] in ["up", "down"]:
    command = sys.argv[1]
else:
    sys.exit(f"""Usage: {sys.argv[0]} <command>
    <command> must be either 'up' or 'down'""")

# Generate the config.
docker_compose_config = "services:"
project_dir = Path(__file__).resolve().parent.parent.parent
network_name = get_config.get_network_name(default="xdmod-data-network")
for python_version in [
    get_config.get_min_python_version(),
    get_config.get_max_python_version(),
]:
    container_name = get_config.get_container_name(
        (
            "python-min"
            if python_version == get_config.get_min_python_version()
            else "python-max"
        ),
        default=f"xdmod-data-python-{python_version}",
    )
    if container_name != "null":
        docker_compose_config += f"""
  {container_name}:
    image: cimg/python:{python_version}
    container_name: {container_name}
    networks:
      - {network_name}
    tty: true
    user: root
    volumes:
      - {project_dir}:/home/circleci/project
"""
for image in get_config.get_xdmod_images():
    container_name = get_config.get_container_name(image, default=image)
    docker_compose_config += f"""
  {container_name}:
    image: tools-ext-01.ccr.xdmod.org/xdmod:{image}
    container_name: {container_name}
    networks:
      - {network_name}
"""
docker_compose_config += f"""
networks:
  {network_name}:
    name: {network_name}
"""


# Run the Docker Compose command.
def run(command):
    subprocess.run(
        f"docker compose -f - {command} --remove-orphans".split(),
        input=docker_compose_config,
        text=True,
        check=True,
    )


if command == "up":
    # run("up -d --pull always")
    run("up -d")
elif command == "down":
    run("down")
