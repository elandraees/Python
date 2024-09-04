from unittest import TestCase
from services.account_service import *
from services.user_access_service import *
from services.access_service import *
from services.user_service import *
from util.regression_database_util import *
from tests.test_data import *
from flask import Flask, request, jsonify
import requests
from base64 import b64encode
from requests.auth import HTTPBasicAuth

local_base_url = 'http://127.0.0.1:5001/accounts/v1'
account_create_path = '/create'
account_auth_path = '/authenticate'
user_create_path = '/user/create'
get_user_path = '/user'
update_user_access = '/access/update'
remove_user_access = '/access/remove'


class Test(TestCase):

    # @classmethod
    # def setUpClass(cls):
    #     account_delete = 'truncate accounts'
    #     controls_delete = 'truncate access_controls'
    #     users_delete = 'truncate users'
    #     account_support_requests_delete = 'truncate account_support_requests'
    #     api_log_delete = 'truncate api_log'
    #     user_access_controls_delete = 'truncate user_access_controls'
    #     insert_or_update_db_record(account_delete, ())
    #     insert_or_update_db_record(users_delete, ())
    #     insert_or_update_db_record(controls_delete, ())
    #     insert_or_update_db_record(account_support_requests_delete, ())
    #     insert_or_update_db_record(api_log_delete, ())
    #     insert_or_update_db_record(user_access_controls_delete, ())

    def test_1(self):
        account_delete = 'truncate accounts'
        controls_delete = 'truncate access_controls'
        users_delete = 'truncate users'
        account_support_requests_delete = 'truncate account_support_requests'
        api_log_delete = 'truncate api_log'
        user_access_controls_delete = 'truncate user_access_controls'
        insert_or_update_db_record(account_delete, ())
        insert_or_update_db_record(users_delete, ())
        insert_or_update_db_record(controls_delete, ())
        insert_or_update_db_record(account_support_requests_delete, ())
        insert_or_update_db_record(api_log_delete, ())
        insert_or_update_db_record(user_access_controls_delete, ())

    # Create accounts and main users
    def test_2(self):
        # Create an account
        create_account(account_1)
        create_account(account_2)

    # Create access controls
    def test_3(self):
        create_access_control({
            "control_id": 10000,
            "name": "Account Access",
            "description": "Allows user super access to the account"
        })

    # Test account creation failure
    def test_4(self):
        with self.assertRaises(Exception):
            create_account(account_3)

    # Create new user for account 1
    def test_5(self):
        # Get auth token of main user of account 1
        response = requests.get(local_base_url + account_auth_path,
                                auth=HTTPBasicAuth(account_1['username'], account_1['password']))
        response_json = response.json()
        account_1_token = response_json['result']['token']
        self.assertTrue(len(account_1_token) > 0)

        # Create new user using the account token
        response = requests.post(local_base_url + user_create_path,
                                 headers={'Authorization': 'Bearer ' + account_1_token},
                                 json=account_1_user_2)
        response_json = response.json()
        self.assertTrue(response_json['success'] == 'true')

    # Test various account access rules using the token of each user
    def test_6(self):
        response = requests.get(local_base_url + account_auth_path,
                                auth=HTTPBasicAuth(account_1['username'], account_1['password']))
        response_json = response.json()
        account_1_token = response_json['result']['token']

        response = requests.get(local_base_url + account_auth_path,
                                auth=HTTPBasicAuth(account_2['username'], account_2['password']))
        response_json = response.json()
        account_2_token = response_json['result']['token']

        response = requests.get(local_base_url + account_auth_path,
                                auth=HTTPBasicAuth(account_1_user_2['username'], account_1_user_2['password']))
        response_json = response.json()
        account_1_user_2_token = response_json['result']['token']

        # Get main user using main user token (true)
        response = requests.get(local_base_url + get_user_path + "?username=" + account_1['username'],
                                headers={'Authorization': 'Bearer ' + account_1_token})
        response_json = response.json()
        self.assertTrue(response_json['success'] == 'true')

        # Get main user using user 2 token (false)
        response = requests.get(local_base_url + get_user_path + "?username=" + account_1['username'],
                                headers={'Authorization': 'Bearer ' + account_1_user_2_token})
        self.assertTrue(response.status_code == 401)

        # Get user 2 using main user token (true)
        response = requests.get(local_base_url + get_user_path + "?username=" + account_1_user_2['username'],
                                headers={'Authorization': 'Bearer ' + account_1_token})
        response_json = response.json()
        self.assertTrue(response_json['success'] == 'true')

        # Get user 2 using user 2 token (true)
        response = requests.get(local_base_url + get_user_path + "?username=" + account_1_user_2['username'],
                                headers={'Authorization': 'Bearer ' + account_1_user_2_token})
        response_json = response.json()
        self.assertTrue(response_json['success'] == 'true')

        # Get account 1 main user using account 2 main user token (false)
        response = requests.get(local_base_url + get_user_path + "?username=" + account_1['username'],
                                headers={'Authorization': 'Bearer ' + account_2_token})
        self.assertTrue(response.status_code == 401)

        # Get account 1 user 2 using account 2 main user token (false)
        response = requests.get(local_base_url + get_user_path + "?username=" + account_1_user_2['username'],
                                headers={'Authorization': 'Bearer ' + account_2_token})
        self.assertTrue(response.status_code == 401)

        # Grant account 1 user 2 super access to account 1
        response = requests.post(local_base_url + update_user_access + "?username=" + account_1_user_2['username'],
                                 headers={'Authorization': 'Bearer ' + account_2_token},
                                 json={'control_ids': [constants.ACCOUNT_ACCESS_CONTROL_ID]})
        self.assertTrue(response.status_code == 401)

        response = requests.post(local_base_url + update_user_access + "?username=" + account_1_user_2['username'],
                                 headers={'Authorization': 'Bearer ' + account_1_token},
                                 json={'control_ids': [constants.ACCOUNT_ACCESS_CONTROL_ID]})
        response_json = response.json()
        self.assertTrue(response_json['success'] == 'true')

        # User 2 should be able to access account main user now
        response = requests.get(local_base_url + get_user_path + "?username=" + account_1['username'],
                                headers={'Authorization': 'Bearer ' + account_1_user_2_token})
        response_json = response.json()
        self.assertTrue(response_json['success'] == 'true')

    # Test various account and user update rules
    def test_7(self):
        response = requests.get(local_base_url + account_auth_path,
                                auth=HTTPBasicAuth(account_1['username'], account_1['password']))
        response_json = response.json()
        account_1_token = response_json['result']['token']

        response = requests.get(local_base_url + account_auth_path,
                                auth=HTTPBasicAuth(account_2['username'], account_2['password']))
        response_json = response.json()
        account_2_token = response_json['result']['token']

        response = requests.get(local_base_url + account_auth_path,
                                auth=HTTPBasicAuth(account_1_user_2['username'], account_1_user_2['password']))
        response_json = response.json()
        account_1_user_2_token = response_json['result']['token']

        # Remove super user access from user 2

    def test_100(self):
        account_delete = 'truncate accounts'
        controls_delete = 'truncate access_controls'
        users_delete = 'truncate users'
        account_support_requests_delete = 'truncate account_support_requests'
        api_log_delete = 'truncate api_log'
        user_access_controls_delete = 'truncate user_access_controls'
        insert_or_update_db_record(account_delete, ())
        insert_or_update_db_record(users_delete, ())
        insert_or_update_db_record(controls_delete, ())
        insert_or_update_db_record(account_support_requests_delete, ())
        insert_or_update_db_record(api_log_delete, ())
        insert_or_update_db_record(user_access_controls_delete, ())
