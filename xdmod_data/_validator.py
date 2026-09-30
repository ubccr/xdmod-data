from datetime import date, timedelta
import xdmod_data._error_messages as _error_messages
import xdmod_data._utilities as _utilities

_PARAM_TYPES = {
    "xdmod_host": "string",
    "duration": "string or an object with 2 items",
    "realm": "string",
    "metric": "string",
    "dimension": "string",
    "filters": "mapping whose keys are strings and whose values are strings or sequences of strings",
    "dataset_type": "string",
    "aggregation_unit": "string",
    "fields": "sequence of strings",
    "show_progress": "Boolean",
    "service_provider": "string",
}


def _assert_runtime_context(in_runtime_context):
    if not in_runtime_context:
        raise RuntimeError(_error_messages.OUTSIDE_RUNTIME_CONTEXT) from None


def _assert_type(param, value):
    if _PARAM_TYPES[param] == "string":
        expected_type = str
    elif _PARAM_TYPES[param] == "Boolean":
        expected_type = bool
    else:  # pragma: nocover
        raise TypeError(
            "Internal error: no handling defined for type '{_PARAM_TYPES[param]}'"
        ) from None
    if not isinstance(value, expected_type):
        raise TypeError(
            _error_messages.TYPE_ERROR(param, _PARAM_TYPES[param])
        ) from None
    return value


def _validate_get_data_params(data_warehouse, aggregate_descriptor, params):
    results = {}
    results["start_date"], results["end_date"] = __validate_duration(params["duration"])
    results["realm"] = aggregate_descriptor._get_data_id(
        "realms",
        params["realm"],
    )
    results["metric"] = aggregate_descriptor._get_data_id(
        "metrics",
        params["metric"],
        results["realm"],
    )
    results["dimension"] = aggregate_descriptor._get_data_id(
        "dimensions",
        params["dimension"],
        results["realm"],
    )
    results["dimension"] = _find_dimension_id(
        descriptors,
        results["realm"],
        params["dimension"],
    )
    results["filters"] = __validate_filters(
        data_warehouse,
        aggregate_descriptor,
        results["realm"],
        params["filters"],
    )
    results["dataset_type"] = __find_str_in_sequence(
        params["dataset_type"],
        ("timeseries", "aggregate"),
        "dataset_type",
    )
    results["aggregation_unit"] = __find_str_in_sequence(
        params["aggregation_unit"],
        _get_aggregation_units(),
        "aggregation_unit",
    )
    return results


def _validate_get_raw_data_params(
    data_warehouse,
    aggregate_descriptor,
    raw_descriptor,
    params,
):
    results = {}
    results["start_date"], results["end_date"] = __validate_duration(params["duration"])
    results["realm"] = raw_descriptor._get_data_id("realms", params["realm"])
    results["fields"] = __validate_raw_fields(
        raw_descriptor,
        results["realm"],
        params["fields"],
    )
    results["realm"] = _find_raw_realm_id(descriptors, params["realm"])
    results["fields"] = __validate_raw_fields(
        data_warehouse,
        params["realm"],
        params["fields"],
    )
    results["filters"] = __validate_filters(
        data_warehouse,
        aggregate_descriptor,
        results["realm"],
        params["filters"],
    )
    results["show_progress"] = _assert_type(
        "show_progress",
        params["show_progress"],
    )
    return results


def _get_durations():
    this_year = date.today().year
    six_years_ago = this_year - 6
    last_seven_years = tuple(
        map(str, reversed(range(six_years_ago, this_year + 1))),
    )
    return (
        "Yesterday",
        "7 day",
        "30 day",
        "90 day",
        "Month to date",
        "Previous month",
        "Quarter to date",
        "Previous quarter",
        "Year to date",
        "Previous year",
        "1 year",
        "2 year",
        "3 year",
        "5 year",
        "10 year",
    ) + last_seven_years


def _get_aggregation_units():
    return (
        "Auto",
        "Day",
        "Month",
        "Quarter",
        "Year",
    )


def _find_raw_realm_id(descriptors, realm):
    return __find_id_in_descriptor(
        descriptors._get_raw(),
        "realm",
        realm,
    )


def __validate_duration(duration):
    if isinstance(duration, str):
        duration = __find_str_in_sequence(
            duration,
            _get_durations(),
            "duration",
        )
        start_date, end_date = __get_dates_from_duration(duration)
    else:
        try:
            start_date, end_date = duration
        except (TypeError, ValueError) as error:
            raise type(error)(
                _error_messages.TYPE_ERROR("duration", _PARAM_TYPES["duration"])
            ) from None
    return (start_date, end_date)


def __validate_filters(data_warehouse, aggregate_descriptor, realm, filters):
    try:
        result = {}
        for dimension in filters:
            dimension_id = aggregate_descriptor._get_data_id(
                "dimensions",
                dimension,
                realm,
            )
            filter_values = filters[dimension]
            if isinstance(filter_values, str):
                filter_values = [filter_values]
            result[dimension_id] = []
            valid_filter_values = data_warehouse.get_filter_values(
                realm,
                dimension,
            )
            for filter_value in filter_values:
                filter_value_id = _utilities._get_id_from_data_frame(
                    filter_value,
                    valid_filter_values,
                    "filter value",
                    realm,
                    dimension,
                )
                result[dimension_id].append(filter_value_id)
        return result
    except TypeError:
        raise TypeError(
            _error_messages.TYPE_ERROR("filters", _PARAM_TYPES["filters"])
        ) from None


def __find_str_in_sequence(value, sequence, label):
    if not isinstance(value, str):
        raise TypeError(
            _error_messages.TYPE_ERROR(label, _PARAM_TYPES[label])
        ) from None
    transformed_value = __lowercase_and_remove_spaces(value)
    for valid_value in sequence:
        transformed_valid_value = __lowercase_and_remove_spaces(valid_value)
        if transformed_valid_value == transformed_value:
            return valid_value
    raise KeyError(
        _error_messages.VALUE_NOT_FOUND(label, value, valid_values=sequence)
    ) from None


def __validate_raw_fields(data_warehouse, realm, fields):
    type_error_message = _error_messages.TYPE_ERROR("fields", _PARAM_TYPES["fields"])
    try:
        results = []
        for field in fields:
            if not isinstance(field, str):
                raise TypeError(type_error_message) from None
            new_field = __find_value_in_df("field", valid_raw_fields, field, realm)
            results.append(new_field)
        return results
    except TypeError:
        raise TypeError(type_error_message) from None


def __find_id_in_descriptor(descriptor, name, value, realm=None):
    _assert_type(name, value)
    for id_ in descriptor:
        if id_ == value or descriptor[id_]["label"] == value:
            return id_
    raise KeyError(_error_messages.VALUE_NOT_FOUND(name, value, realm)) from None


def __find_metric_or_dimension_id(descriptors, realm, m_or_d, value):
    return __find_id_in_descriptor(
        descriptors._get_aggregate()[realm][m_or_d + "s"],
        m_or_d,
        value,
        realm,
    )


def __get_dates_from_duration(duration):
    today = date.today()
    yesterday = today + timedelta(days=-1)
    last_week = today + timedelta(days=-7)
    last_month = today + timedelta(days=-30)
    last_quarter = today + timedelta(days=-90)
    this_month_start = date(today.year, today.month, 1)
    if today.month == 1:  # pragma: no cover
        last_full_month_start_year = today.year - 1
        last_full_month_start_month = 12
    else:  # pragma: no cover
        last_full_month_start_year = today.year
        last_full_month_start_month = today.month - 1
    last_full_month_start = date(
        last_full_month_start_year,
        last_full_month_start_month,
        1,
    )
    last_full_month_end = this_month_start + timedelta(days=-1)
    this_quarter_start = date(
        today.year,
        ((today.month - 1) // 3) * 3 + 1,
        1,
    )
    if today.month < 4:  # pragma: no cover
        last_quarter_start_year = today.year - 1
    else:  # pragma: no cover
        last_quarter_start_year = today.year
    last_quarter_start = date(
        last_quarter_start_year,
        (((today.month - 1) - ((today.month - 1) % 3) + 9) % 12) + 1,
        1,
    )
    last_quarter_end = this_quarter_start + timedelta(days=-1)
    this_year_start = date(today.year, 1, 1)
    this_year_end = date(today.year, 12, 31)
    previous_year_start = date(today.year - 1, 1, 1)
    previous_year_end = date(today.year - 1, 12, 31)
    durations_to_dates = {
        "Yesterday": (yesterday, yesterday),
        "7 day": (last_week, today),
        "30 day": (last_month, today),
        "90 day": (last_quarter, today),
        "Month to date": (this_month_start, today),
        "Previous month": (last_full_month_start, last_full_month_end),
        "Quarter to date": (this_quarter_start, today),
        "Previous quarter": (last_quarter_start, last_quarter_end),
        "Year to date": (this_year_start, today),
        "Previous year": (previous_year_start, previous_year_end),
        "1 year": (__date_add_years(today, -1), today),
        "2 year": (__date_add_years(today, -2), today),
        "3 year": (__date_add_years(today, -3), today),
        "5 year": (__date_add_years(today, -5), today),
        "10 year": (__date_add_years(today, -10), today),
        str(today.year): (this_year_start, this_year_end),
        str(__date_add_years(today, -1).year): (
            previous_year_start,
            previous_year_end,
        ),
    }
    for num_years in range(2, 7):
        durations_to_dates[str(__date_add_years(today, -num_years).year)] = (
            date(today.year - num_years, 1, 1),
            date(today.year - num_years, 12, 31),
        )
    return durations_to_dates[duration]


def __lowercase_and_remove_spaces(value):
    return value.lower().replace(" ", "")


def __date_add_years(old_date, year_delta):
    # Make dates behave like Ext.JS, i.e., if a date is specified
    # with a day value that is too big, add days to the last valid
    # day in that month, e.g., 2023-02-31 becomes 2023-03-03.
    new_date_year = old_date.year + year_delta
    new_date_day = old_date.day
    days_above = 0
    keep_going = True
    while keep_going:
        try:
            new_date = date(new_date_year, old_date.month, new_date_day)
            keep_going = False
        except ValueError:  # pragma: no cover
            new_date_day -= 1
            days_above += 1
    return new_date + timedelta(days=days_above)
