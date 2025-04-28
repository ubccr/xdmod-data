import json
import os
import re
import requests
from urllib.parse import urlencode
import warnings
import xdmod_data._validator as _validator
from xdmod_data.__version__ import __title__, __version__


class _HttpRequester:
    def __init__(self, xdmod_host):
        self.__in_runtime_context = False
        _validator._assert_str('xdmod_host', xdmod_host)
        xdmod_host = re.sub('/+$', '', xdmod_host)
        self.__xdmod_host = xdmod_host
        try:
            self.__api_token = os.environ['XDMOD_API_TOKEN']
        except KeyError:
            raise KeyError(
                '`XDMOD_API_TOKEN` environment variable has not been set.',
            ) from None
        self.__headers = {
            'Authorization': 'Bearer ' + self.__api_token,
            'User-Agent': __title__ + ' Python v' + __version__,
        }
        self.__requests_session = None
        self.__raw_data_limit = None

    def _start_up(self):
        self.__in_runtime_context = True
        self.__requests_session = requests.Session()

    def _tear_down(self):
        if self.__requests_session is not None:
            self.__requests_session.close()
        self.__in_runtime_context = False

    def _request_data(self, params):
        return self.__request(
            path='/controllers/user_interface.php',
            post_fields=self.__get_data_post_fields(params),
        )

    def _request_raw_data(self, params):
        url_params = self.__get_raw_data_url_params(params)
        data = []
        fields = None
        response = self.__request(
            path='/rest/v1/warehouse/raw-data?' + url_params,
            post_fields=None,
            stream=True,
        )
        num_rows_read = 0
        # Once XDMoD ?.? is no longer supported, only the else branch will
        # be needed:
        if response.headers['Content-Type'] == 'application/json-seq':
            for line in response.iter_lines():
                line_text = line.decode('utf-8').replace('\x1e', '')
                (data, fields) = self.__process_raw_data_response_row(
                    line_text,
                    num_rows_read,
                    params['show_progress'],
                    data,
                    fields,
                )
                num_rows_read += 1
            if params['show_progress']:
                self.__print_progress_msg(num_rows_read, 'DONE\n')
        else:
            # The data stream consists of pairs of lines where the second
            # line contains the row we care about and the first line
            # contains the hex size of the second line.
            is_first_line_in_pair = True
            for line in response.iter_lines():
                line_text = line.decode('utf-8')
                if is_first_line_in_pair:
                    last_line_size = line_text
                # The last line will be of size 0 and should not be
                # processed.
                elif last_line_size != '0':
                    (data, fields) = self.__process_raw_data_response_row(
                        line_text,
                        num_rows_read,
                        params['show_progress'],
                        data,
                        fields,
                    )
                    num_rows_read += 1
                is_first_line_in_pair = not is_first_line_in_pair
            if params['show_progress']:
                self.__print_progress_msg(num_rows_read, 'DONE\n')
            if last_line_size != '0':
                warnings.warn(
                    'Connection closed before all data were received!',
                    RuntimeWarning,
                )
        return (data, fields)

    def _request_filter_values(self, realm_id, dimension_id):
        limit = 10000
        data = []
        num_rows = limit
        offset = 0
        while num_rows == limit:
            response = self._request_json(
                path='/controllers/metric_explorer.php',
                post_fields={
                    'operation': 'get_dimension',
                    'realm': realm_id,
                    'dimension_id': dimension_id,
                    'start': offset,
                    'limit': limit,
                },
            )
            data += response['data']
            num_rows = len(response['data'])
            offset += limit
        return data

    def _request_json(self, path, post_fields=None):
        response = self.__request(path, post_fields)
        return json.loads(response.text)

    def __request(self, path='', post_fields=None, stream=False):
        _validator._assert_runtime_context(self.__in_runtime_context)
        url = self.__xdmod_host + path
        if post_fields:
            response = self.__requests_session.post(
                url,
                headers=self.__headers,
                data=post_fields,
                stream=stream,
            )
        else:
            response = self.__requests_session.get(
                url,
                headers=self.__headers,
                stream=stream,
            )
        if response.status_code != 200:
            msg = ''
            try:
                response_json = json.loads(response.text)
                msg = ': ' + response_json['message']
            except json.JSONDecodeError:  # pragma: no cover
                pass
            if response.status_code == 401:
                msg = (
                    ': Make sure XDMOD_API_TOKEN is set to a valid API token.'
                )
            raise RuntimeError(
                'Error ' + str(response.status_code) + msg,
            ) from None
        return response

    def __get_data_post_fields(self, params):
        post_fields = {
            'operation': 'get_data',
            'start_date': params['start_date'],
            'end_date': params['end_date'],
            'realm': params['realm'],
            'statistic': params['metric'],
            'group_by': params['dimension'],
            'dataset_type': params['dataset_type'],
            'aggregation_unit': params['aggregation_unit'],
            'format': 'csv',
        }
        for dimension in params['filters']:
            post_fields[dimension + '_filter'] = ','.join(
                params['filters'][dimension],
            )
        return post_fields

    def __get_raw_data_url_params(self, params):
        results = {
            'realm': params['realm'],
            'start_date': params['start_date'],
            'end_date': params['end_date'],
        }
        if (params['fields']):
            results['fields'] = ','.join(params['fields'])
        if (params['filters']):
            for dimension in params['filters']:
                results['filters[' + dimension + ']'] = ','.join(
                    params['filters'][dimension],
                )
        return urlencode(results)

    def __process_raw_data_response_row(
        self,
        line_text,
        num_rows_read,
        show_progress,
        data,
        fields,
    ):
        line_json = json.loads(line_text)
        if num_rows_read == 0:
            fields = line_json
        else:
            data.append(line_json)
            # Only print every 10,000 rows to avoid I/O rate
            # errors.
            if show_progress and num_rows_read % 10000 == 0:
                self.__print_progress_msg(num_rows_read, '\r')
        return (data, fields)

    def __print_progress_msg(self, num_rows, end='\n'):
        progress_msg = (
            'Got ' + str(num_rows) + ' row' + ('' if num_rows == 1 else 's')
            + '...'
        )
        print(progress_msg, end=end)
