# xdmod-data

As part of the Data Analytics Framework for [XDMoD](https://open.xdmod.org),
this Python package provides API access to the data warehouse of instances of
Open XDMoD.

The package can be installed from PyPI via `pip install xdmod-data`.

Existing installations can be upgraded via `pip install --upgrade xdmod-data`.

The package has dependencies on [NumPy](https://pypi.org/project/numpy/),
[Pandas](https://pypi.org/project/pandas/),
[Plotly](https://pypi.org/project/plotly/), and
[Requests](https://pypi.org/project/requests/).

Example usage is documented through Jupyter notebooks in the
[xdmod-notebooks](https://github.com/ubccr/xdmod-notebooks) repository.

## Compatibility with Open XDMoD

Specific versions of this package are compatible with specific versions of Open
XDMoD as indicated in the table below.

| `xdmod-data` versions | Open XDMoD versions    |
| --------------------- | ---------------------- |
| 1.1.0                 | 11.0.x                 |
| 1.0.3, 1.0.2, 1.0.1   | 11.0.1, 11.0.0, 10.5.x |
| 1.0.0                 | 10.5.x                 |

## API Token Access

The Data Analytics Framework can be used within an XDMoD-hosted JupyterHub
(such as is available for [ACCESS XDMoD](https://xdmod.access-ci.org)), in
which case authentication happens automatically through XDMoD. Otherwise,
authentication occurs via API tokens. To obtain an API token from the XDMoD
portal, follow the instructions
[here](https://open.xdmod.org/data-analytics-framework.html#api-token-generation).

## Feedback / Feature Requests

We welcome your feedback and feature requests for the Data Analytics Framework
for XDMoD via email: ccr-xdmod-help@buffalo.edu.

## Support

For support, please see [this page](https://open.xdmod.org/support.html). If
you email for support, please include the following:
* `xdmod-data` version number, obtained by running this Python code:
    ```
    from xdmod_data import __version__
    print(__version__)
    ```
* Operating system version.
* A description of the problem you are experiencing.
* Detailed steps to reproduce the problem.

## License

`xdmod-data` is released under the GNU Lesser General Public License ("LGPL")
Version 3.0. See the [LICENSE](LICENSE) file for details.

## References

When referencing the Data Analytics Framework for XDMoD, please cite the
following publication:

> Weeden, A., White, J.P., DeLeon, R.L., Rathsam, R., Simakov, N.A., Saeli, C.,
> and Furlani, T.R. The Data Analytics Framework for XDMoD. _SN COMPUT. SCI._
> 5, 462 (2024). https://doi.org/10.1007/s42979-024-02789-2

When referencing XDMoD, please cite the following publication:

> Jeffrey T. Palmer, Steven M. Gallo, Thomas R. Furlani, Matthew D. Jones,
> Robert L. DeLeon, Joseph P. White, Nikolay Simakov, Abani K. Patra, Jeanette
> Sperhac, Thomas Yearke, Ryan Rathsam, Martins Innus, Cynthia D. Cornelius,
> James C. Browne, William L. Barth, Richard T. Evans, "Open XDMoD: A Tool for
> the Comprehensive Management of High-Performance Computing Resources",
> *Computing in Science & Engineering*, Vol 17, Issue 4, 2015, pp. 52-62.
> DOI:[10.1109/MCSE.2015.68](https://doi.org/10.1109/MCSE.2015.68)
