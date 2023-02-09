import os
import pandas
import unittest
import xdmod.datawarehouse as xdw


class TestDataWarehouse(unittest.TestCase):
    __INVALID_STR = 'asdlkfjsdlkfisdjkfjd'
    __VALID_REALM = 'Jobs'
    __XDMOD_URL = 'https://xdmod-dev.ccr.xdmod.org'

    def setUp(self):
        self.__valid_dw = xdw.DataWarehouse(self.__XDMOD_URL)

    def tearDown(self):
        pass

    def test___init___KeyError_XDMOD_USER(self):
        old_environ = dict(os.environ)
        os.environ.clear()
        try:
            with self.assertRaises(KeyError):
                xdw.DataWarehouse(self.__XDMOD_URL)
        finally:
            os.environ.clear()
            os.environ.update(old_environ)

    def test___init___KeyError_XDMOD_PASS(self):
        old_environ = dict(os.environ)
        os.environ.clear()
        os.environ['XDMOD_USER'] = self.__INVALID_STR
        try:
            with self.assertRaises(KeyError):
                xdw.DataWarehouse(self.__XDMOD_URL)
        finally:
            os.environ.clear()
            os.environ.update(old_environ)

    def test___init___TypeError_xdmod_host(self):
        with self.assertRaises(TypeError):
            xdw.DataWarehouse(2)

    def test___init___TypeError_api_key(self):
        with self.assertRaises(TypeError):
            xdw.DataWarehouse(self.__XDMOD_URL, 2)

    def test___enter___RuntimeError_xdmod_host_malformed(self):
        with self.assertRaises(RuntimeError):
            with xdw.DataWarehouse(''):
                pass

    def test___enter___RuntimeError_xdmod_host_unresolved(self):
        with self.assertRaises(RuntimeError):
            with xdw.DataWarehouse('asdfsdf.xdmod.org'):
                pass

    def test___enter___RuntimeError_xdmod_host_bad_port(self):
        with self.assertRaises(RuntimeError):
            with xdw.DataWarehouse('xdmod-dev.ccr.xdmod.org:0'):
                pass

    def test___enter___RuntimeError_xdmod_host_unsupported_protocol(self):
        with self.assertRaises(RuntimeError):
            with xdw.DataWarehouse('asdklsdfj://sdlkfs'):
                pass

    def test_get_realms_return_type(self):
        with self.__valid_dw:
            self.assertIsInstance(self.__valid_dw.get_realms(), tuple)

    def test_get_realms_RuntimeError_outside_context(self):
        with self.assertRaises(RuntimeError):
            self.__valid_dw.get_realms()

    def test_get_metrics_return_type(self):
        with self.__valid_dw:
            self.assertIsInstance(self.__valid_dw.get_metrics(self.__VALID_REALM),
                                                              pandas.core.frame.DataFrame)

    def test_get_metrics_KeyError(self):
        with self.__valid_dw:
            with self.assertRaises(KeyError):
                self.__valid_dw.get_metrics(self.__INVALID_STR)

    def test_get_metrics_TypeError(self):
        with self.__valid_dw:
            with self.assertRaises(TypeError):
                self.__valid_dw.get_realms(2)

    def test_get_metrics_RuntimeError_outside_context(self):
        with self.assertRaises(RuntimeError):
            self.__valid_dw.get_metrics(self.__VALID_REALM)

    def test_get_dimensions_return_type(self):
        with self.__valid_dw:
            self.assertIsInstance(self.__valid_dw.get_dimensions(self.__VALID_REALM),
                                                                 pandas.core.frame.DataFrame)

    def test_get_dimensions_KeyError(self):
        with self.__valid_dw:
            with self.assertRaises(KeyError):
                self.__valid_dw.get_dimensions(self.__INVALID_STR)

    def test_get_dimensions_TypeError(self):
        with self.__valid_dw:
            with self.assertRaises(TypeError):
                self.__valid_dw.get_realms(2)

    def test_get_dimensions_RuntimeError_outside_context(self):
        with self.assertRaises(RuntimeError):
            self.__valid_dw.get_dimensions(self.__VALID_REALM)

    def test_get_dataset_KeyError_duration(self):
        with self.__valid_dw:
            with self.assertRaises(KeyError):
                self.__valid_dw.get_dataset(duration=self.__INVALID_STR)

    def test_get_dataset_KeyError_realm(self):
        with self.__valid_dw:
            with self.assertRaises(KeyError):
                self.__valid_dw.get_dataset(realm=self.__INVALID_STR)

    def test_get_dataset_KeyError_metric(self):
        with self.__valid_dw:
            with self.assertRaises(KeyError):
                self.__valid_dw.get_dataset(metric=self.__INVALID_STR)

    def test_get_dataset_KeyError_dimension(self):
        with self.__valid_dw:
            with self.assertRaises(KeyError):
                self.__valid_dw.get_dataset(dimension=self.__INVALID_STR)

    def test_get_dataset_KeyError_filters(self):
        with self.__valid_dw:
            with self.assertRaises(KeyError):
                self.__valid_dw.get_dataset(filters={self.__INVALID_STR})

    def test_get_dataset_KeyError_dataset_type(self):
        with self.__valid_dw:
            with self.assertRaises(KeyError):
                self.__valid_dw.get_dataset(dataset_type=self.__INVALID_STR)

    def test_get_dataset_KeyError_aggregation_unit(self):
        with self.__valid_dw:
            with self.assertRaises(KeyError):
                self.__valid_dw.get_dataset(aggregation_unit=self.__INVALID_STR)

    def test_get_dataset_RuntimeError_outside_context(self):
        with self.assertRaises(RuntimeError):
            self.__valid_dw.get_dataset()

    def test_get_dataset_TypeError_duration(self):
        with self.__valid_dw:
            with self.assertRaises(TypeError):
                self.__valid_dw.get_dataset(duration=1)

    def test_get_dataset_TypeError_realm(self):
        with self.__valid_dw:
            with self.assertRaises(TypeError):
                self.__valid_dw.get_dataset(realm=1)

    def test_get_dataset_TypeError_metric(self):
        with self.__valid_dw:
            with self.assertRaises(TypeError):
                self.__valid_dw.get_dataset(metric=1)

    def test_get_dataset_TypeError_dimension(self):
        with self.__valid_dw:
            with self.assertRaises(TypeError):
                self.__valid_dw.get_dataset(dimension=1)

    def test_get_dataset_TypeError_filters(self):
        with self.__valid_dw:
            with self.assertRaises(TypeError):
                self.__valid_dw.get_dataset(filters=1)

    def test_get_dataset_TypeError_dataset_type(self):
        with self.__valid_dw:
            with self.assertRaises(TypeError):
                self.__valid_dw.get_dataset(dataset_type=1)

    def test_get_dataset_TypeError_aggregation_unit(self):
        with self.__valid_dw:
            with self.assertRaises(TypeError):
                self.__valid_dw.get_dataset(aggregation_unit=1)

    def test_get_dataset_ValueError_duration(self):
        with self.__valid_dw:
            with self.assertRaises(ValueError):
                self.__valid_dw.get_dataset(duration=('1', '2', '3'))

    def test_get_dataset_RuntimeError_start_date_malformed(self):
        with self.__valid_dw:
            with self.assertRaises(RuntimeError):
                self.__valid_dw.get_dataset(duration=(self.__INVALID_STR,
                                                      '2022-01-01'))

    def test_get_dataset_RuntimeError_end_date_malformed(self):
        with self.__valid_dw:
            with self.assertRaises(RuntimeError):
                self.__valid_dw.get_dataset(duration=('2022-01-01',
                                                      self.__INVALID_STR))


if __name__ == '__main__':
    unittest.main()
