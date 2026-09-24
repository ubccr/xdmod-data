def _get_id_from_data_frame(
    value,
    data_frame,
    data_type_label,
    realm=None,
):
    matches = data_frame.index[
        (data_frame.index == value) | (data_frame["label"] == value)
    ]
    if matches.empty:
        return None
    return matches[0]
