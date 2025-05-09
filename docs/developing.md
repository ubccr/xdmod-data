# Instructions for developers

## Testing the code

A testing script is available in `tests/ci/bootstrap.sh`. It requires Docker
Compose and `yq`.

To test with the notebooks in `xdmod-notebooks`, you can edit their first code
cell to replace `xdmod-data` and its version constraints with the following,
replacing `username` with your username and `branch-name` with the name of the
branch:
```
git+https://github.com/username/xdmod-data.git@branch-name
```

## Contributing a Pull Request (PR)

1. Get the PR reviewed.
1. Once the PR is approved and merged,
    1. In the release prep draft PR for the version under development:
        1. In `CHANGELOG.md`:
            1. Add the PR you just merged.
            1. If needed, update the summary of the version under development
               and its compatibility with Open XDMoD versions.
        1. In `README.md`:
            1. If needed, update the Open XDMoD compatibility matrix.
    1. If needed, port/backport the PR to other development branches, and
       update their release prep draft PRs as well.

## Releasing a new version

1. In the version's release prep draft PR:
    1. In `xdmod_data/__version__.py`, make sure the version number is updated.
    1. In `README.md`, make sure the Open XDMoD compatibility matrix is
       updated.
    1. In `CHANGELOG.md`, update the release date of the version and make sure
       it has a summary of the changes in the version and indicates the
       compatibility with Open XDMoD versions.
1. After the PR is approved (but not merged yet), follow these steps in a
   cloned copy of the branch:
    1. Start up a virtual environment, e.g.:
        ```
        python3 -m venv ~/xdmod-data-build-env
        source ~/xdmod-data-build-env/bin/activate
        ```
        Your command prompt should now start with `(xdmod-data-build-env)`.
    1. Make sure the required packages are installed:
        ```
        python3 -m pip install --upgrade pip build setuptools twine
        ```
    1. Build the built distribution:
        ```
        python3 -m build --wheel
        ```
    1. Validate `setup.cfg`, e.g., for version 1.0.1:
        ```
        version=1.0.1
        twine check dist/xdmod_data-${version}-py3-none-any.whl
        ```
        Make sure you receive `PASSED`.
    1. Upload the built distribution to TestPyPI:
        ```
        twine upload --repository testpypi dist/xdmod_data-${version}-py3-none-any.whl
        ```
        Enter your TestPyPI API token.
    1. Go to https://test.pypi.org/project/xdmod-data and confirm that
       everything looks right.
    1. Upload the built distribution to PyPI:
        ```
        twine upload dist/xdmod_data-${version}-py3-none-any.whl
        ```
        Enter your PyPI username and password.
    1. Go to https://pypi.org/project/xdmod-data and confirm the new version is
       the latest release.
1. Merge the PR.
1. Go to [create a new release on
   GitHub](https://github.com/ubccr/xdmod-data/releases/new) and:
    1. Click `Choose a tag`.
    1. Type in a tag similar to `v1.0.0` and choose `Create new tag`.
    1. Choose the correct target based on the major version you are developing.
    1. Make the release title the same as the tag name (e.g., `v1.0.0`).
    1. Where it says `Describe this release`, paste in the contents of the
       release's section in `CHANGELOG.md`. Note that single newlines are
       interpreted as line breaks, so you may need to reformat the description
       to break the lines where you want them to break. Use the `Preview` to
       make sure it looks right.
    1. Where it says `Attach binaries`, attach the built distribution (the
       `.whl` file) that was uploaded to PyPI.
    1. Click `Publish release`.
    1. Go to the [GitHub
       milestones](https://github.com/ubccr/xdmod-data/milestones) and close
       the milestone for the version.

## After release

1. If you just released a new major version (e.g., `2.0.0`),
    1. Create a branch off `main` for that major version (e.g., `v2.x.y`).
    1. For each major version below that major version (e.g., `1.x.y`), make a
       PR to that branch that updates `README.md` to add a link to the new
       version's README to the list under `For documentation of other
       versions:` and updates the main development branch's link text in that
       list to the next major version (e.g., `v3.x.y (main development
       branch)`). Get the PR approved and merged.
    1. In a PR to the `main` branch, update the `README.md` under the main
       heading, in the sentence that begins `This documentation is for ...`,
       update the version number in the bold text (e.g., `**v3.x.y (main
       development branch)**`. Get the PR approved and merged.
1. If you just released a new minor or patch version of a version that is not
   the most recent major version under development (e.g., `v1.1.0`):
    1. For each major version above that version's major version (e.g.,
      `v2.x.y`), in that major version's release prep draft PR:
        1. In `CHANGELOG.md`, make sure the version just released is present
           but that the PR numbers match the ones that were merged into the
           major branch whose Pull Request you are currently creating, NOT the
           branch that the release was tagged on.
        1. In the `README.md`, update the Open XDMoD compatibility matrix.
        1. Get the PR approved and merged.
1. In a PR to the same branch you just released:
    1. In `xdmod_data/__version__.py`, make sure the version number is updated
       to a development pre-release of the next version, e.g., `3.0.0.dev01`.
    1. In `README.md`:
        1. If you just released a new major version:
            1. Under the main heading, in the sentence that begins `This
               documentation is for ...`, update the bold text from e.g.,
               `**v2.x.y (main development branch)**` to, e.g., `the **v2.x.y**
               versions`.
            1. In the list under `For documentation of other versions:`, update
               the main development branch's link text to the next major
               version (e.g., `v3.x.y (main development branch)`).
    1. Get the PR approved and merged.
1. For each new version under development:
    1. Go to the [GitHub
       milestones](https://github.com/ubccr/xdmod-data/milestones) and add a
       milestone for the new version under development.
    1. Create a release prep draft PR for the new version under development:
        1. In `CHANGELOG.md`:
            1. Add a heading for the new version under development with a date of
               `XXXX-XX-XX`.
            1. If you already know what will be done in the new version under
               development, write a summary of it.
            1. Add the expected compatibility with Open XDMoD versions.
        1. In `README.md`, add the new version under development to the Open XDMoD
           compatibility matrix.
        1. In `xdmod_data/__version__.py`, change the version number to the new
           version under development.
