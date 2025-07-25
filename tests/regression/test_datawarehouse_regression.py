from datetime import date
from dotenv import load_dotenv
import json
import numpy
import os
import pandas
from pathlib import Path
import pytest
from xdmod_data.warehouse import DataWarehouse

XDMOD_VERSION = os.environ['XDMOD_VERSION']
TOKEN_PATH = '~/.xdmod-data-token'


load_dotenv(Path(os.path.expanduser(TOKEN_PATH)), override=True)
# When outputting dataframes for debugging, don't truncate any of the output.
pandas.set_option('display.max_rows', None)
pandas.set_option('display.max_columns', None)
pandas.set_option('display.width', None)
pandas.set_option('display.max_colwidth', None)


@pytest.fixture(scope='module')
def valid_dw():
    with DataWarehouse() as dw:
        yield dw


def __assert_dfs_equal(
    data_file,
    actual,
    dtype='object',
    index_col='id',
    columns_name=None,
    override_default_data=False,
):
    data_dir = __get_data_dir(override_default_data)
    if 'GENERATE_DATA_FILES' in os.environ:  # pragma: no cover
        actual.to_csv(data_dir + '/' + data_file)
    else:
        expected = pandas.read_csv(
            data_dir + '/' + data_file,
            dtype=dtype,
            index_col=index_col,
            keep_default_na=False,
            na_values=[''],
        ).fillna(numpy.nan)
        expected.columns = expected.columns.astype('string')
        expected.columns.name = columns_name
        if index_col == 'Time':
            expected.index = pandas.to_datetime(expected.index)
        assert expected.equals(actual), (
            '\nEXPECTED:\n' + str(expected) + '\nACTUAL:\n' + str(actual)
        )


def __get_data_dir(override_default_data=False):
    data_dir = os.path.dirname(__file__) + '/data/' + (
        XDMOD_VERSION if override_default_data
        else 'default'
    )
    if 'GENERATE_DATA_FILES' in os.environ:  # pragma: no cover
        try:
            os.mkdir(data_dir)
        except FileExistsError:
            pass
    return data_dir


@pytest.mark.parametrize(
    'additional_params, number, csv_title',
    [
        (
            {},
            '54748',
            'raw-data-every-1000-no-fields-no-filters.csv',
        ),
        (
            {
                'fields':
                (
                    'Local Job Id',
                    'Quality of Service',
                    'GPUs',
                    'Start Time',
                    'Department',
                ),
                'filters':
                {
                    'Resource':
                    [
                        'mortorq',
                        'frearson',
                    ],
                },
            },
            '33346',
            'raw-data-every-1000-with-fields-and-filters.csv',
        ),
    ],
    ids=('no-fields-and-filters', 'with-fields-and-filters'),
)
def test_get_raw_data(valid_dw, capsys, additional_params, number, csv_title):
    defult_params = {
        'duration': ('2016-01-01', '2016-12-31'),
        'realm': 'Jobs',
        'show_progress': True,
    }
    params = {**defult_params, **additional_params}
    data = valid_dw.get_raw_data(**params).iloc[::1000]
    data.index = data.index.astype('string')
    __assert_dfs_equal(
        csv_title,
        data,
        dtype='string',
        index_col=0,
        override_default_data=(
            XDMOD_VERSION in ['xdmod-11-0', 'xdmod-11-0-dev']
        ),
    )
    assert 'Got ' + number + ' rows...DONE' in capsys.readouterr().out


def __assert_descriptor_dfs_equal(
    data_file,
    actual,
    override_default_data=False,
):
    __assert_dfs_equal(
        data_file,
        actual,
        dtype='string',
        override_default_data=override_default_data,
    )


def test_describe_realms(valid_dw):
    __assert_descriptor_dfs_equal(
        'realms.csv',
        valid_dw.describe_realms(),
    )


def test_describe_metrics(valid_dw):
    __assert_descriptor_dfs_equal(
        'jobs-metrics.csv',
        valid_dw.describe_metrics('Jobs'),
        override_default_data=(
            XDMOD_VERSION in ['xdmod-11-0', 'xdmod-11-0-dev']
        ),
    )


def test_describe_dimensions(valid_dw):
    __assert_descriptor_dfs_equal(
        'jobs-dimensions.csv',
        valid_dw.describe_dimensions('Jobs'),
        override_default_data=(
            XDMOD_VERSION in ['xdmod-11-0', 'xdmod-11-0-dev']
        ),
    )


def test_get_filter_values(valid_dw):
    __assert_descriptor_dfs_equal(
        'jobs-pi-group-filter-values.csv',
        valid_dw.get_filter_values('Jobs', 'PI Group'),
    )


def test_get_data_filter_user(valid_dw):
    # Make sure the filter validation works for a user whose list position is
    # greater than 10000 — this will raise an exception if it doesn't work.
    valid_dw.get_data(
        duration=('2016-01-01', '2017-12-31'),
        realm='Jobs',
        metric='CPU Hours: Total',
        dataset_type='aggregate',
        filters={'User': '10332'},
    )


@pytest.mark.parametrize(
    'aggregation_unit,data_file',
    [
        ('Month', 'jobs-2016-2017-month.csv'),
        ('Quarter', 'jobs-2016-2017-quarters.csv'),
        ('Year', 'jobs-2016-2017-years.csv'),
    ],
    ids=('month', 'quarter', 'year'),
)
def test_get_data(valid_dw, aggregation_unit, data_file):
    data = valid_dw.get_data(
        duration=('2016-01-01', '2017-12-31'),
        realm='Jobs',
        metric='CPU Hours: Total',
        aggregation_unit=aggregation_unit,
    )
    __assert_dfs_equal(
        data_file,
        data,
        index_col='Time',
        columns_name='Metric',
        dtype={'CPU Hours: Total': 'Float64'},
    )


def test_get_aggregation_units(valid_dw):
    expected_agg_units = ('Auto', 'Day', 'Month', 'Quarter', 'Year')
    actual_agg_units = valid_dw.get_aggregation_units()
    assert expected_agg_units == actual_agg_units


def test_get_durations(valid_dw):
    expected_durations = [
        'Yesterday',
        '7 day',
        '30 day',
        '90 day',
        'Month to date',
        'Previous month',
        'Quarter to date',
        'Previous quarter',
        'Year to date',
        'Previous year',
        '1 year',
        '2 year',
        '3 year',
        '5 year',
        '10 year',
    ]
    today_date = date.today()
    current_year = today_date.year
    for count in range(0, 7):
        year = current_year - count
        year = str(year)
        expected_durations.append(year)
    actual_durations = list(valid_dw.get_durations())
    assert expected_durations == actual_durations


@pytest.mark.parametrize(
    'service_provider', [[None], ['screw']],
)
def test_get_resources(valid_dw, service_provider):
    # get_resources is not supported in XDMoD < 11.0.2.
    if XDMOD_VERSION != 'xdmod-11-0':
        with open(__get_data_dir() + '/' + 'resources.json') as data_file:
            data = json.load(data_file)
        assert data == valid_dw.get_resources()
