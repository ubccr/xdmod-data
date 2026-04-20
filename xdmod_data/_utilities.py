import pandas as pd
import warnings


def _get_id_from_data_frame(
    value,
    data_frame,
    data_type_label,
    realm=None,
):
    mask = (
        (data_frame.index == value)
        | (data_frame['label'] == value)
    )
    deprecated_names_mask = pd.Series(False, index=data_frame.index)
    if 'deprecated_names' in data_frame.columns:
        deprecated_names_mask = data_frame['deprecated_names'].apply(
            lambda deprecated_names: (
                not pd.isna(deprecated_names)
                and value in deprecated_names
            ),
        )
        mask |= deprecated_names_mask
    matches = data_frame.index[mask]
    if matches.empty:
        return None
    data_id = matches[0]
    __warn_if_deprecated(
        value,
        data_frame,
        data_type_label,
        data_id,
        deprecated_names_mask,
        realm,
    )
    return data_id


def __warn_if_deprecated(
    name,
    data_frame,
    data_type_label,
    data_id,
    deprecated_names_mask,
    realm,
):
    realm_text = ''
    warn = False
    if realm is not None:
        realm_text = f" in the '{realm}' realm"
    if 'deprecated' in data_frame.columns:
        deprecated = data_frame.loc[data_id, 'deprecated']
        if not pd.isna(deprecated) and deprecated:
            alternative_text = data_frame.loc[data_id, 'description'].replace(
                'DEPRECATED: ',
                '',
            )
            warn = True
    if not warn and deprecated_names_mask.any():
        label = data_frame.loc[data_id, 'label']
        alternative = label
        if data_id != label:
            alternative = f"{data_id}' or '{label}"
        alternative_text = f"Use '{alternative}' instead."
        warn = True
    if warn:
        warnings.warn(
            (
                f"The {data_type_label} name '{name}'{realm_text} is"
                f' deprecated and will be removed in a future version of'
                f" XDMoD. {alternative_text}"
            ),
            FutureWarning,
            stacklevel=7,
        )
