# xdmod-data Changelog

## v1.1.0 (2025-07-17)

This release adds support for running the package in an XDMoD-hosted
JupyterHub, adds a method for retrieving data about resources (from XDMoD
portals running version 11.0.2 or greater), adds a module with helper functions
for making Jupyter reports, and fixes a bug in retrieving raw data.

It is compatible with Open XDMoD version 11.0.x.

- Remove unnecessary request made when runtime context is entered
  ([\#74](https://github.com/ubccr/xdmod-data/pull/74)).
- Remove Open XDMoD 10.5 support
  ([\#75](https://github.com/ubccr/xdmod-data/pull/75)).
- Raise runtime error if raw data stream is closed unexpectedly.
  ([\#80](https://github.com/ubccr/xdmod-data/pull/80)).
- Add `get_resources` method to the API
  ([\#83](https://github.com/ubccr/xdmod-data/pull/83)).
- Add support for running in an XDMoD-hosted JupyterHub
  ([\#84](https://github.com/ubccr/xdmod-data/pull/84)).
- Add report module ([\#86](https://github.com/ubccr/xdmod-data/pull/86)).

## v1.1.0 (XXXX-XX-XX)

This release adds support for running the package in an XDMoD-hosted
JupyterHub, adds a method for retrieving data about resources (currently
limited to ACCESS XDMoD but will be available in a future version of Open
XDMoD), adds a submodule with helper functions for making Jupyter reports, and
fixes a bug in retrieving raw data.

It is compatible with Open XDMoD version 11.0.x.

- Remove unnecessary request made when runtime context is entered
  ([\#74](https://github.com/ubccr/xdmod-data/pull/74)).
- Remove Open XDMoD 10.5 support
  ([\#75](https://github.com/ubccr/xdmod-data/pull/75)).
- Raise runtime error if raw data stream is closed unexpectedly.
  ([\#80](https://github.com/ubccr/xdmod-data/pull/80)).

## v1.0.3 (2025-01-30)

This release fixes a `ValueError` that occurs with the Plotly `timeseries`
template.

It is compatible with Open XDMoD versions 11.0.1, 11.0.0, and 10.5.x.

- Implement 100% test coverage
  ([\#27](https://github.com/ubccr/xdmod-data/pull/27)).
- Update Flake8 rules ([\#28](https://github.com/ubccr/xdmod-data/pull/28)).
- Change to using CircleCI instead of GitHub Actions for continuous integration
  ([\#48](https://github.com/ubccr/xdmod-data/pull/48),
  [\#49](https://github.com/ubccr/xdmod-data/pull/49),
  [\#51](https://github.com/ubccr/xdmod-data/pull/51),
  [\#52](https://github.com/ubccr/xdmod-data/pull/52),
  [\#59](https://github.com/ubccr/xdmod-data/pull/59)).
- Fix Plotly template ValueError
  ([\#61](https://github.com/ubccr/xdmod-data/pull/61)).

## v1.0.2 (2024-10-31)

This release fixes an `IOPub` error that can occur when calling
`get_raw_data()` with `show_progress=True`.

It is compatible with Open XDMoD versions 11.0.1, 11.0.0, and 10.5.x.

- Document Open XDMoD compatibility in changelog
  ([\#31](https://github.com/ubccr/xdmod-data/pull/31)).
- Fix IOPub error when showing progress with `get_raw_data()`
  ([\#39](https://github.com/ubccr/xdmod-data/pull/39)).

## v1.0.1 (2024-09-27)

This release has bug fixes, performance improvements, and updates for
compatibility, tests, and documentation.

It is compatible with Open XDMoD versions 11.0.1, 11.0.0, and 10.5.x.

- Add borders to README images
  ([\#12](https://github.com/ubccr/xdmod-data/pull/12)).
- Create `PULL_REQUEST_TEMPLATE.md`
  ([\#13](https://github.com/ubccr/xdmod-data/pull/13)).
- Add types of changes to pull request template
  ([\#15](https://github.com/ubccr/xdmod-data/pull/15)).
- Add Changelog ([\#17](https://github.com/ubccr/xdmod-data/pull/17)).
- Update tests and testing instructions
  ([\#14](https://github.com/ubccr/xdmod-data/pull/14)).
- Remove limit on number of results returned from `get_filter_values()`
  ([\#21](https://github.com/ubccr/xdmod-data/pull/21)).
- Add citation for the DAF paper
  ([\#23](https://github.com/ubccr/xdmod-data/pull/23)).
- Add a "Feedback / Feature Requests" section to the README
  ([\#22](https://github.com/ubccr/xdmod-data/pull/22)).
- Improve performance of validation of filters and raw fields
  ([\#18](https://github.com/ubccr/xdmod-data/pull/18)).
- Fix bug with trailing slashes in `xdmod_host`
  ([\#24](https://github.com/ubccr/xdmod-data/pull/24)).
- Use streaming for raw data requests
  ([\#19](https://github.com/ubccr/xdmod-data/pull/19)).
- Specify minimum version numbers for dependencies
  ([\#25](https://github.com/ubccr/xdmod-data/pull/25)).

## v1.0.0 (2023-07-21)

Initial release.

Compatible with Open XDMoD version 10.5.x.
