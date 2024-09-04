# Account Service
- This is a multi tier account service. Users can register accounts and create multiple users for the accounts.
- This project also includes the ability to assign access roles to users and use them across other micro services.
- The project structure follows a mix of the MVC, repository and services pattern.
- Even though the DB used in this project is a postgres one, you can easily replace the database_util.py file with a new one and just implement the same methods.

Languages and Technologies Used:
- Python
- Flask
- Postgres
- JWT authentication

### API Doc:
 ### Account API
API methods relating to the main account/s

#### 1. Create Account

    Method: POST
    Endpoint: /accounts/v1/create

    Headers:
        Content-Type    application/json
        Secret-Key

    Example Body:
        {
            "account_name": "Business1",
            "first_name": "One",
            "last_name": "Person",
            "email_address": "One@gmail.com",
            "contact_number": "0712341111",
            "username": "oneperson",
            "password": "MAGT!qwefvsssr1"
        }

    Example Response:
        {
          "message": "Successfully created account",
          "result": {
            "account_name": "Business1",
            "cell_number": "0712341111",
            "create_date": "Mon, 02 Sep 2024 09:54:44 GMT",
            "email_address": "One@gmail.com",
            "id": 22,
            "last_update": "Mon, 02 Sep 2024 09:54:44 GMT",
            "status": "ACTIVE",
            "username": "oneperson"
          },
          "success": true
        }

#### 2. Update Account

    Method: POST
    Endpoint: /accounts/v1/update

    Headers:
        Content-Type    application/json
        Authorization   Bearer Token (JWT Auth token)

    Example Body:
        {
            "account_name": "Business12",
            "first_name": "One123",
            "last_name": "Person",
            "email_address": "one@gmail.com",
            "contact_number": "0712341111",
            "username": "oneperson123",
            "password": "MAGT!qwefvsssr1",
            "status": "ACTIVE"
        }

    Example Response:
        {
          "message": "Successfully updated account",
          "result": {
            "account_name": "Business12",
            "cell_number": "0712341111",
            "create_date": "Mon, 02 Sep 2024 09:54:44 GMT",
            "email_address": "one@gmail.com",
            "last_update": "2024-09-02 09:55:42",
            "status": "ACTIVE"
          },
          "success": true
        }

#### 3. Authenticate Account
        Method: GET
        Endpoint: /accounts/v1/authenticate

        Headers:
           Authorization    Basic Auth (Username, Password)

        Example Response:
            {
              "message": "",
              "result": {
                "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2NvdW50X2lkIjoyMiwiYWNjb3VudF91c2VybmFtZSI6Im9uZXBlcnNvbiIsInVzZXJuYW1lIjoib25lcGVyc29uIiwiZXhwIjoxNzI1MjcwOTIyfQ.7hDAN4JN6L2xgVaqvaKMZsmVka4TTK6q-rCuwm1o5hw"
              },
              "success": true
            }

#### 3. Get Account Details
        Method: GET
        Endpoint: /accounts/v1

        Headers:
           Authorization    Bearer Token (JWT Auth token)

        Example Response:
            {
              "message": "",
              "result": {
                "account_name": "Business12",
                "cell_number": "0712341111",
                "create_date": "Mon, 02 Sep 2024 09:54:44 GMT",
                "email_address": "one@gmail.com",
                "id": 22,
                "last_update": "Mon, 02 Sep 2024 09:55:42 GMT",
                "status": "ACTIVE",
                "username": "oneperson"
              },
              "success": true
            }

 ### User API
API methods relating to the users of an account

#### 1. Create User

    Method: POST
    Endpoint: /accounts/v1/user/create

    Headers:
        Content-Type    application/json
        Authorization    Bearer Token (JWT Auth token)

    Example Body:
        {
            "first_name": "OneOne",
            "last_name": "Person",
            "email_address": "One1@gmail.com",
            "contact_number": "0712341111",
            "username": "oneperson123",
            "password": "MAGT!qwefvsssr1"
        }

    Example Response:
        {
          "message": "Successfully created user",
          "result": {
            "first_name": "OneOne",
            "last_name": "Person",
            "email_address": "One1@gmail.com",
            "contact_number": "0712341111",
            "username": "oneperson123",
          },
          "success": true
        }

#### 2. Update User

    Method: POST
    Endpoint: /accounts/v1/user/update/:username

    Path Variables:
        username

    Headers:
        Content-Type    application/json
        Authorization    Bearer Token (JWT Auth token)

    Example Body:
        {
            "first_name": "OneOne",
            "last_name": "Person",
            "email_address": "One1@gmail.com",
            "contact_number": "0712341111",
            "password": "MAGT!qwefvsssr1"
        }

    Example Response:
        {
          "message": "Successfully created user",
          "result": {
            "first_name": "OneOne",
            "last_name": "Person",
            "email_address": "One1@gmail.com",
            "contact_number": "0712341111",
            "username": "oneperson123",
          },
          "success": true
        }

#### 3. Get Users
        Method: GET
        Endpoint: /accounts/v1/users

        Headers:
           Authorization    Bearer Token (JWT Auth token)

        Example Response:
            {
              "message": "",
              "result": [
                {
                  "cell_number": "0712341111",
                  "create_date": "Mon, 02 Sep 2024 09:54:44 GMT",
                  "email_address": "one@gmail.com",
                  "last_update": "Mon, 02 Sep 2024 09:55:43 GMT",
                  "name": "One123 Person",
                  "status": "ACTIVE",
                  "user_id": 5,
                  "username": "oneperson"
                }
              ],
              "success": true
            }

#### 4. Get User
        Method: GET
        Endpoint: /accounts/v1/user?username=<username>

        Headers:
           Authorization    Bearer Token (JWT Auth token)

        Example Response:
            {
              "message": "",
              "result": [
                {
                  "cell_number": "0712341111",
                  "create_date": "Mon, 02 Sep 2024 09:54:44 GMT",
                  "email_address": "one@gmail.com",
                  "last_update": "Mon, 02 Sep 2024 09:55:43 GMT",
                  "name": "One123 Person",
                  "status": "ACTIVE",
                  "user_id": 5,
                  "username": "oneperson"
                }
              ],
              "success": true
            }


 ### Access Control API
API methods relating to the users access

#### 1. Create Access Control

    Method: POST
    Endpoint: /accounts/v1/access/create

    Headers:
        Content-Type    application/json
        Secret-Key    

    Example Body:
        {
            "control_id":10000,
            "name":"Account Access",
            "description":"Allows user super access to the account"
        }

    Example Response:
        {
          "message": "Successfully created control",
          "result": {
            },
          "success": true
        }

#### 2. Update User Access Control
        Method: POST
        Endpoint: /accounts/v1/access/update?username=<>

        Headers:
           Authorization    Bearer Token (JWT Auth token)

        Example Body:
            {
                "control_ids":[10000]
            }

        Example Response:
            {
              "message": "Successfully updated access",
              "result": {
                },
              "success": true
            }

#### 3. Remove User Access Control List
        Method: GET
        Endpoint: /accounts/v1/access/remove?username=<>

        Headers:
           Authorization    Bearer Token (JWT Auth token)

        Example Body:
            {
                "control_ids":[10000]
            }

        Example Response:
            {
              "message": "Successfully removed access",
              "result": {
                },
              "success": true
            }

#### 4. Can User Access Control
        Method: GET
        Endpoint: /accounts/v1/access/can_access?username=<>&control_id=<>

        Headers:
           Authorization    Bearer Token (JWT Auth token)

        Example Response:
            {
              "message": "",
              "result": {
                    true
                },
              "success": true
            }

#### 4. Get User Access Control List
        Method: GET
        Endpoint: /accounts/v1/access/get_access?username=

        Headers:
           Authorization    Bearer Token (JWT Auth token)

        Example Response:
            {
              "message": "",
              "result": {
                    [10000, 100001]
                },
              "success": true
            }

    