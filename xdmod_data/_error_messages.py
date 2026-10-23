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


def TYPE_ERROR(param, type_description=None):
    if param == "duration":
        type_description = "string or an object with 2 items"
    elif param == "filters":
        type_description = "mapping whose keys are strings and whose values are strings or sequences of strings"
    elif param == "fields":
        type_description = "sequence of strings"
    return f"`{param}` must be a {type_description}."


def VALUE_NOT_FOUND(name, value, realm=None, dimension=None, valid_values=None):
    if name == "field":
        value_text = "Raw field"
    elif name == "filter value":
        value_text = "Filter value"
    else:
        value_text = f"Value for `{name}`"
    realm_text = "" if realm is None else f" in the '{realm}' realm"
    dimension_text = "" if dimension is None else f" for the '{dimension}' dimension"
    valid_values_sentence = ""
    if valid_values is not None:
        valid_values_str = "', '".join(valid_values)
        valid_values_sentence = f" Value values are: '{valid_values_str}'"
    return f"{value_text} not found{dimension_text}{realm_text}: '{value}'.{valid_values_sentence}"


def GET_RESOURCES_NOT_SUPPORTED(host):
    return (
        f"The requested XDMoD portal ({host}) is not running a version of"
        " XDMoD that supports the `get_resources` method."
    )
