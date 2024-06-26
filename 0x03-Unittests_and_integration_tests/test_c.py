#!/usr/bin/env python3

"""
Test module for the client.

This module contains unit tests for the GithubOrgClient
class in the client module.
"""

import unittest
from unittest.mock import patch
from parameterized import parameterized, parameterized_class
import client
from client import GithubOrgClient
from utils import memoize
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """
    Test cases for the GithubOrgClient class.
    """

    @parameterized.expand([
        ("google"),
        ("abc"),
    ])
    @patch('client.get_json', return_value={"payload": True})
    def test_org(self, org, mock_get):
        """
        Test the org method of GithubOrgClient class.

        Args:
            org (str): The organization name to test.
            mock_get (MagicMock): Mock object for get_json function.
        """
        test = GithubOrgClient(org)
        result = test.org
        self.assertEqual(result, mock_get.return_value)
        mock_get.assert_called_once()

    def test_public_repos_url(self):
        """
        Test the _public_repos_url method of GithubOrgClient class.
        """

        @patch('client.get_json', return_value={"payload": True})
        @memoize
        def test_public_repos_url(self, _public_repos_url):
            """
            Test the _public_repos_url method of GithubOrgClient class.

            Args:
                _public_repos_url (MagicMock):
                Mock object for get_json function.
         """
            test = GithubOrgClient("_public_repos_url")
            test_public_repos_url = test._public_repos_url
            self.assertEqual(test_public_repos_url,
                             _public_repos_url.return_value)
            mock_get.assert_called_once()

            @patch('client.get_json', return_value=[{"name": "Alx"}])
            def test_public_repos(self, mock_get_json):
                """
                Test the public_repos method of GithubOrgClient class.
                Args:
                mock_get_json (MagicMock): Mock object for get_json function.
                """
                with patch.object(GithubOrgClient, '_public_repos_url',
                                  new_callable=PropertyMock) \
                        as mock_public_repos_url:
                    mock_public_repos_url.return_value = \
                        "https://api.github.com/orgs/test_org/repos"

                    test = GithubOrgClient("test_org")
                    test_public_repos = test.public_repos
                    for repo in test_public_repos:
                        self.assertEqual(repo, {"name": "Alx"})
                    mock_public_repos_url.assert_called_once()
                    mock_get_json.assert_called_once()

            @parameterized.expand([
                ({'license': {'key': 'my_license'}}, 'my_license', True),
                ({'license': {'key': 'other_license'}}, 'my_license', False),
            ])
            def test_has_license(self, repo, license_key, expected):
                """
                Test the has_license method of GithubOrgClient class.
                Args:
                repo (dict): The repository to test.
                license_key (str): The license key to test.
                expected (bool): The expected result.
                """
                test = GithubOrgClient("test_org")
                result = test.has_license(repo, license_key)
                self.assertEqual(result, expected)


@parameterized_class(
    ('org_payload', 'repos_payload', 'expected_repos', 'apache2_repos'),
    [(TEST_PAYLOAD[0][0], TEST_PAYLOAD[0][1], TEST_PAYLOAD[0][2],
      TEST_PAYLOAD[0][3])]
)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """
    Integration test for the GithubOrgClient.public_repos method
    """

    @classmethod
    def setUpClass(self):
        """
        Set up function for TestIntegrationGithubOrgClient class.
        Sets up the patcher for the get_json function.
        """
        self.patcher = patch('client.get_json')
        self.mock_get_json = self.patcher.start()
        self.mock_get_json.side_effect = [
            self.org_payload, self.repos_payload
        ]

    @classmethod
    def tearDownClass(self):
        """
        Tear down function for TestIntegrationGithubOrgClient class.
        Stops the patcher for the get_json function.
        """
        self.patcher.stop()
