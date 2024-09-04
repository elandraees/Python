from controllers.v1.controller_helper import *

account_bp = Blueprint('accounts', __name__, url_prefix='/accounts/v1')

api_method = ""


@account_bp.after_request
def after_request(response):
    try:
        api_log_repo.log_request(api_method, get_account_id(), request, response)
    except Exception as e:
        print(e)
    return response


@account_bp.route('/create', methods=['POST'])
@authenticate_secret
def create_account():
    global api_method
    api_method = "CREATE_ACCOUNT"
    json = request.json
    if json is None:
        return api_response.get_error_response("No body found", [], 400)

    try:
        account: Account = account_service.create_account(json)
        return api_response.get_success_response("Successfully created account", account.to_json_include_id())
    except Exception as e:
        return api_response.get_error_response("An error has occurred", json_util.parse_str_to_json(str(e)), 400)


@account_bp.route('/list', methods=['GET'])
@authenticate_secret
def get_accounts():
    global api_method
    api_method = "GET_ACCOUNT_LIST"
    try:
        accounts: [dict] = account_service.get_account_list()
        return api_response.get_success_response("", accounts)
    except Exception as e:
        return api_response.get_error_response("An error has occurred", json_util.parse_str_to_json(str(e)), 400)


# Token belonging to the main account will have the username = account_username
@account_bp.route('/authenticate', methods=['GET'])
@authenticate_user_password
def get_user_auth_token():
    global api_method
    api_method = "GET_USER_AUTH"
    try:
        token_dict = user_service.get_user_auth_token(get_username())
        return api_response.get_success_response("", token_dict)
    except Exception as e:
        return api_response.get_error_response("An error has occurred", json_util.parse_str_to_json(str(e)), 400)


# Only the main user can access this
@account_bp.route('/', methods=['GET'])
@authenticate_token_and_main_user
def get_account():
    global api_method
    api_method = "GET_ACCOUNT"
    try:
        account: Account = account_service.get_account(get_account_username())
        return api_response.get_success_response("", account.to_json_include_id())
    except Exception as e:
        return api_response.get_error_response("An error has occurred", json_util.parse_str_to_json(str(e)), 400)


@account_bp.route('/update', methods=['POST'])
@authenticate_token_and_main_user
def update_account():
    global api_method
    api_method = "UPDATE_ACCOUNT"
    json = request.json
    if json is None:
        return api_response.get_error_response("No body found", [], 400)

    try:
        account_data: Account = account_service.update_account(json, get_account_username())
        return api_response.get_success_response("Successfully updated account", account_data.to_json())
    except Exception as e:
        return api_response.get_error_response("An error has occurred", json_util.parse_str_to_json(str(e)), 400)
