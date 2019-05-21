import pytest
import os
import warnings
import json
import requests
from DataAnalysis import csv_handle
from collections import OrderedDict


class TestCsvHandle(object):

    test_csv_content = """Terytorium;Przystąpiło/zdało;Płeć;Rok;Liczba osób
Polska;przystąpiło;kobiety;2000;200
Pomorze;przystąpiło;kobiety;2000;50
Pomorze;zdało;kobiety;2000;20
Wielkopolska;przystąpiło;kobiety;2000;40
Wielkopolska;zdało;kobiety;2010;20
"""

    @pytest.fixture(autouse=True)
    def create_data_file(self, tmpdir):
        self.tmpdir = tmpdir.strpath
        d = tmpdir.mkdir("resource")
        self.csv_dir = d.join("test.csv")

        self.csv_dir.write(self.test_csv_content)

    single_prams = [
        ({'Terytorium': "Polska"},  1),
        ({'Terytorium': "Pomorze"},  2),
        ({'Rok': '2000'},  4),
        ({'Płeć': 'kobiety'},  5),
        ({'Liczba osób': '20'},  2),
        ({'Przystąpiło/zdało': 'przystąpiło'},  3),
    ]

    multiple_prams = [
        ({'Terytorium': "Pomorze", 'Przystąpiło/zdało': "zdało"},  1),
        ({'Terytorium': 'Wielkopolska', 'Rok': '2000'},  1),
        ({'Terytorium': 'Pomorze', 'Rok': '2000',
          'Płeć': 'kobiety', 'Liczba osób': '50'}, 1)
    ]

    list_params = [
        ({'Terytorium': ['Pomorze', 'Wielkopolska'],
          'Przystąpiło/zdało':"zdało"},  2),
        ({'Rok': ['2000', '2010']},  5),
        ({'Płeć': ['kobiety', 'mężczyźni'], 'Liczba osób':['200', '20']}, 3)
    ]

    def test_file_path_assignment(self):
        handle = csv_handle.CSVHandle("test.csv")

        assert handle.csv_file_path == "test.csv"

    def test_output_type(self):
        handle = csv_handle.CSVHandle(self.csv_dir)
        all_data = handle.get_csv_data()

        assert type(all_data) is list
        assert type(all_data[0]) is type(OrderedDict())

    def test_wrong_path_exception(self):
        handle = csv_handle.CSVHandle("empty.csv")
        with pytest.raises(FileNotFoundError):
            handle.get_csv_data()

    def test_default_read(self):
        handle = csv_handle.CSVHandle(self.csv_dir)
        all_data = handle.get_csv_data()

        assert len(all_data) is 5

    @pytest.mark.parametrize("kwargs, expected_size", single_prams)
    def test_find_by_single_param(self, kwargs, expected_size):
        handle = csv_handle.CSVHandle(self.csv_dir)

        data = handle.get_csv_data(**kwargs)

        assert len(data) is expected_size

    @pytest.mark.parametrize("kwargs, expected_size", multiple_prams)
    def test_find_by_multiple_param(self, kwargs, expected_size):
        handle = csv_handle.CSVHandle(self.csv_dir)

        data = handle.get_csv_data(**kwargs)

        assert len(data) is expected_size

    @pytest.mark.parametrize("kwargs, expected_size", list_params)
    def test_find_by_list_param(self, kwargs, expected_size):
        handle = csv_handle.CSVHandle(self.csv_dir)

        data = handle.get_csv_data(**kwargs)

        assert len(data) is expected_size

    def test_find_by_incorrect_param(self):
        handle = csv_handle.CSVHandle(self.csv_dir)

        with pytest.warns(Warning):
            data = handle.get_csv_data(miasto='4')

        assert len(data) is 5

    def test_get_column_names(self):
        handle = csv_handle.CSVHandle(self.csv_dir)

        expected = ['Terytorium', 'Przystąpiło/zdało',
                    'Płeć', 'Rok', 'Liczba osób']
        actual = handle.get_column_names()

        assert actual == expected

    def test_get_data_from_api(self, requests_mock):
        url = 'http://data_api_test.com/jsonapi'
        csv_data = 'http://data.com/csvfile.csv'
        content = {}
        content['data'] = {}
        content['data']['attributes'] = {}
        content['data']['attributes']['file_url'] = csv_data
        requests_mock.get(url, text=json.dumps(content))
        requests_mock.get(csv_data, text=self.test_csv_content)

        save_dir = self.csv_dir + "2"
        handle = csv_handle.CSVHandle(save_dir)
        handle.download_data_from_api(url)

        expected = self.csv_dir.read()
        actual = save_dir.read()
        assert expected == actual

    def test_get_data_from_fail_api(self, requests_mock):
        url = 'http://data_api_test.com/jsonapi'
        csv_data = 'http://data.com/csvfile.csv'
        content = {}
        requests_mock.get(url, text=json.dumps(content))
        requests_mock.get(csv_data, text=self.test_csv_content)

        save_dir = self.csv_dir + "2"
        handle = csv_handle.CSVHandle(save_dir)
        with pytest.raises(Exception):
            handle.download_data_from_api(url)

    def test_get_data_from_fail_find_api(self, requests_mock):
        url = 'http://data_api_test.com/jsonapi'
        csv_data = 'http://data.com/csvfile.csv'
        content = {}
        requests_mock.get(url, text=json.dumps(content))
        requests_mock.get(csv_data, text=self.test_csv_content)

        save_dir = self.csv_dir + "2"
        handle = csv_handle.CSVHandle(save_dir)
        with pytest.raises(Exception, match = r"Can't find info about csv file location in api*"):
            handle.download_data_from_api(url)

    def test_get_data_from_fail_connect(self, requests_mock):
        url = 'http://data_api_test.com/jsonapi'
        csv_data = 'http://data.com/csvfile.csv'
        content = {}
        requests_mock.get(url, exc=requests.exceptions.HTTPError)
        requests_mock.get(csv_data, text=self.test_csv_content)

        save_dir = self.csv_dir + "2"
        handle = csv_handle.CSVHandle(save_dir)
        with pytest.raises(ValueError, match = r"Cannot connect to .* and get csv data" ):
            handle.download_data_from_api(url)