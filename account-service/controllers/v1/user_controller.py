from controllers.v1.controller_helper import *

user_bp = Blueprint('users', __name__, url_prefix='/accounts/v1')

api_method = ""


@user_bp.after_request
def after_request(response):
    try:
        api_log_repo.log_request(api_method, get_account_id(), request, response)
    except Exception as e:
        print(e)
    return response


@user_bp.route('/user/create', methods=['POST'])
@authenticate_token_access_or_main_user(constants.ACCOUNT_ACCESS_CONTROL_ID, constants.EDIT_ALL_USERS_ACCESS_CONTROL_ID)
def create_user():
    global api_method
    api_method = "CREATE_USER"
    json = request.json
    if json is None:
        return api_response.get_error_response("No body found", [], 400)
    try:
        user: User = user_service.create_user(json, get_account_username())
        return api_response.get_success_response("Successfully created user", user.to_json_include_id())
    except Exception as e:
        return api_response.get_error_response("An error has occurred", str(e), 400)


@user_bp.route('/users', methods=['GET'])
@authenticate_token_access_or_main_user(constants.ACCOUNT_ACCESS_CONTROL_ID, constants.EDIT_ALL_USERS_ACCESS_CONTROL_ID,
                                        constants.VIEW_ALL_USERS_ACCESS_CONTROL_ID)
def get_users():
    global api_method
    api_method = "GET_USERS"
    try:
        response = user_service.get_user_list(get_account_id())
        return api_response.get_success_response("", response)
    except Exception as e:
        return api_response.get_error_response("An error has occurred", str(e), 400)


@user_bp.route('/user', methods=['GET'])
@authenticate_token_access_or_self(constants.ACCOUNT_ACCESS_CONTROL_ID, constants.EDIT_ALL_USERS_ACCESS_CONTROL_ID,
                                   constants.VIEW_ALL_USERS_ACCESS_CONTROL_ID)
def get_user():
    global api_method
    api_method = "GET_USER"
    try:
        param_username = request.args.get('username')
        if param_username is None:
            return api_response.get_error_response("An error has occurred", "No username found", 400)

        user: User = user_service.get_user(param_username)
        return api_response.get_success_response("", user.to_json())
    except Exception as e:
        return api_response.get_error_response("An error has occurred", str(e), 400)


@user_bp.route('/user/update', methods=['POST'])
@authenticate_token_access_or_self(constants.ACCOUNT_ACCESS_CONTROL_ID, constants.EDIT_ALL_USERS_ACCESS_CONTROL_ID)
def update_user():
    global api_method
    api_method = "UPDATE_USER"
    json = request.json
    if json is None:
        return api_response.get_error_response("No body found", [], 400)

    try:
        param_username = request.args.get('username')
        if param_username is None:
            return api_response.get_error_response("An error has occurred", "No username found", 400)

        if param_username == get_account_username():
            account_service.update_account(json, param_username)
        else:
            user_service.update_user(json, param_username, get_account_id())
        return api_response.get_success_response("Successfully updated user", "")

    except Exception as e:
        return api_response.get_error_response("An error has occurred", str(e), 400)
