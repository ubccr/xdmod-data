# Generate CircleCI config. This is done so the minimum and maximum Python
# versions do not have to be redundantly declared in multiple files.

import get_config

# Get Python versions.
min_python_version = str(get_config.get_min_python_version())
max_python_version = str(get_config.get_max_python_version())

# Generate the config.
output_config = f"""
version: 2.1

jobs:
  lint:
    docker:
      - image: cimg/python:{max_python_version}
    resource_class: small
    steps:
      - checkout
      - run: python3 ./tests/scripts/install_dependencies.py
      - run: python3 ./tests/scripts/lint.py
"""
for python_version in [min_python_version, max_python_version]:
    output_config += f"""
  test_python_{python_version.replace('.', '_')}:
    docker:
      - image: cimg/python:{python_version}
        name: xdmod-data-python-{python_version}
    """
    for image in get_config.get_xdmod_images():
        output_config += f"""
      - image: tools-ext-01.ccr.xdmod.org/xdmod:{image}
        name: {image}
    """
    output_config += """
    resource_class: small
    steps:
      - checkout
      - run: python3 ./tests/scripts/install_dependencies.py
      - run: python3 ./tests/scripts/setup.py
    """
    if python_version == min_python_version:
        output_config += """
      - run: python3 ./tests/scripts/downgrade_dependencies.py
        """
    output_config += f"""
      - run: python3 ./tests/scripts/run_tests.py
    """
output_config += """
workflows:
  lint:
    jobs:
      - lint
  run_tests:
    jobs:
"""
for python_version in [min_python_version, max_python_version]:
    output_config += f"""
      - test_python_{python_version.replace('.', '_')}
    """

# Output the config.
print(output_config)
