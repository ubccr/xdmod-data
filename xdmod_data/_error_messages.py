MISSING_XDMOD_HOST = (
    "`xdmod_host` parameter or `XDMOD_HOST` environment variable must be set."
)

OUTSIDE_RUNTIME_CONTEXT = (
    "Method is being called outside of the runtime context. Make sure this"
    " method is only called within the body of a `with` statement."
)

HTTP_401 = "Make sure XDMOD_API_TOKEN is set to a valid API token."

JUPYTERHUB = (
    "If running in an XDMoD-hosted JupyterHub, this is likely a server error"
    " from the JupyterHub. If not running in an XDMoD-hosted JupyterHub, make"
    " sure the `XDMOD_API_TOKEN` environment variable is set before the"
    " `DataWarehouse` is constructed; it should be set to a valid API token"
    " obtained from the XDMoD portal."
)

INVALID_DURATION = "`duration` must be a string or an object with 2 items."

INVALID_FILTERS = (
    "`filters` must be a mapping whose keys are strings and whose values are"
    " strings or sequences of strings."
)

INVALID_RAW_FIELDS = "`fields` must be a sequence of strings."


def GET_RESOURCES(host):
    return (
        f"The requested XDMoD portal ({host}) is not running a version of"
        " XDMoD that supports the `get_resources` method."
    )
