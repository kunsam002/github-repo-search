import os
import unittest
import json
import app
from app import fetch_repo_details, index
from mock import patch, MagicMock, Mock


class TestFetchRepo(unittest.TestCase):
    """
    TestCase for the fetch repository details view function
    """

    ############################
    #### setup and cleanup ####
    ############################
    def setUp(self):
        fake_data = str({"apiUrl": "FAKE-12345678"})

        self.request_mock = Mock()
        self.request_mock.method = "POST"
        self.request_mock.data = fake_data
        self.request_mock.form = fake_data

        self.json_mock = MagicMock()

        self.requests_mock = MagicMock()

        self.os_mock = Mock()

        self.results = {"commits": self.json_mock.load(), "fork": self.json_mock.loads().__getitem__(),
                        "forkOwnerBio": self.json_mock.loads().get()}
        self.jsonify_mock = MagicMock(return_value=self.results)

        self.patchall = patch.multiple(app, request=self.request_mock,
                                       json=self.json_mock,
                                       jsonify=self.jsonify_mock,
                                       len=Mock(return_value=2),
                                       requests=self.requests_mock,
                                       os=self.os_mock)
        self.patchall.start()

        self.addCleanup(patch.stopall)

    def test_post_fetch_repo_details_page(self):
        result = app.fetch_repo_details()
        self.assertEqual(self.requests_mock.get.call_count, 3)
        self.assertEqual(self.json_mock.loads.call_count, 6)
        self.assertTrue(self.request_mock.method)
        self.assertTrue(self.jsonify_mock.called)
        self.assertTrue(self.requests_mock.get.called)

        self.assertEqual(result, self.results)

    def test_get_fetch_repo_details_page(self):
        self.request_mock.method = "GET"
        self.jsonify_mock = Mock(return_value={})

        app.fetch_repo_details()

        self.assertEqual(self.requests_mock.get.call_count, 0)
        self.assertFalse(self.jsonify_mock.called)
        self.assertFalse(self.requests_mock.get.called)


class TestIndexPage(unittest.TestCase):
    """
        TestCase for the search git repository view function
    """

    ############################
    #### setup and cleanup ####
    ############################
    def setUp(self):
        self.request_mock = Mock()
        self.request_mock.args.get.return_value = 'test'

        self.requests_mock = MagicMock()
        self.requests_mock.get().status_code = 200

        self.json_mock = MagicMock()

        self.render_template_mock = Mock()

        self.patchall = patch.multiple(app, int=Mock(return_value=2),
                                       request=self.request_mock,
                                       requests=self.requests_mock,
                                       json=self.json_mock,
                                       render_template=self.render_template_mock)
        self.patchall.start()

        self.addCleanup(patch.stopall)

    def test_index_call_with_results(self):
        app.index()
        self.assertEqual(self.requests_mock.get.call_count, 2)
        self.assertEqual(self.request_mock.args.get.call_count, 2)
        self.assertEqual(self.json_mock.loads.call_count, 1)
        self.assertTrue(self.requests_mock.get.called)

    def test_index_call_with_empty_results(self):
        self.requests_mock.get().status_code = 500
        app.index()
        self.assertEqual(self.request_mock.args.get.call_count, 2)
        self.assertEqual(self.json_mock.loads.call_count, 0)
        self.assertTrue(self.requests_mock.get.called)


if __name__ == "__main__":
    unittest.main()
