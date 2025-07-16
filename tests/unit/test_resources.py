import os
from requests import Session
from unittest.mock import patch
from xdmod_data.warehouse import DataWarehouse

VALID_XDMOD_HOST = os.environ['XDMOD_HOST']

class MockResponse:
    def __init__(self, status_code):
        self.status_code = status_code
        self.text = '{ "results": "resourcelist" }'

@patch.object(Session, 'get', return_value=MockResponse(200))
def test_fetch(self):
    with DataWarehouse(VALID_XDMOD_HOST) as dw:
        result = dw.get_resources()
        assert "resourcelist" == result

        result = dw.get_resources("Provider")
        assert "resourcelist" == result
