from controllers.v1.controller_helper import *
import services.user_access_service as user_access_service
import services.access_service as access_service
from models.access_control import AccessControl


access_bp = Blueprint('access', __name__, url_prefix='/accounts/v1/access')

api_method = ""


@access_bp.after_request
def after_request(response):
    try:
        api_log_repo.log_request(api_method, get_account_id(), request, response)
    except Exception as e:
        print(e)
    return response


@access_bp.route('/create', methods=['POST', 'OPTIONS'])
@authenticate_secret
def create_access_control():
    global api_method
    api_method = "CREATE_ACCESS_CONTROL"
    json = request.json
    if json is None:
        return api_response.get_error_response("No body found", [], 400)
    try:
        access_control: AccessControl = access_service.create_access_control(json)
    except Exception as e:
        return api_response.get_error_response("An error has occurred", str(e), 400)

    return api_response.get_success_response("Successfully create control", access_control.to_json())


@access_bp.route('/update', methods=['POST'])
@authenticate_token_access_or_self(constants.ACCOUNT_ACCESS_CONTROL_ID, constants.EDIT_ALL_USERS_ACCESS_CONTROL_ID)
def update_user_access_control():
    global api_method
    api_method = "UPDATE_USER_ACCESS_CONTROL"
    json = request.json
    if json is None:
        return api_response.get_error_response("No body found", [], 400)

    try:
        param_username = request.args.get('username')
        if param_username is None:
            return api_response.get_error_response("An error has occurred", "No username found", 400)

        user_access_service.create_user_controls(json, param_username)
        return api_response.get_success_response("Successfully updated access", "")
    except Exception as e:
        return api_response.get_error_response("An error has occurred", str(e), 400)


@access_bp.route('/remove', methods=['POST'])
@authenticate_token_access_or_self(constants.ACCOUNT_ACCESS_CONTROL_ID, constants.EDIT_ALL_USERS_ACCESS_CONTROL_ID)
def remove_user_access_control():
    global api_method
    api_method = "REMOVE_USER_ACCESS_CONTROL"
    json = request.json
    if json is None:
        return api_response.get_error_response("No body found", [], 400)

    try:
        param_username = request.args.get('username')
        if param_username is None:
            return api_response.get_error_response("An error has occurred", "No username found", 400)
        user_access_service.remove_user_controls(json, param_username)
        return api_response.get_success_response("Successfully removed access", "")
    except Exception as e:
        return api_response.get_error_response("An error has occurred", str(e), 400)


@access_bp.route('/get_access', methods=['GET'])
@authenticate_token_access_or_self(constants.ACCOUNT_ACCESS_CONTROL_ID, constants.EDIT_ALL_USERS_ACCESS_CONTROL_ID,
                                   constants.VIEW_ALL_USERS_ACCESS_CONTROL_ID)
def get_user_access():
    global api_method
    api_method = "CAN_ACCESS"

    user = request.args.get('username')

    try:
        user_access_controls: [UserAccessControl] = user_access_service.get_all_controls_for_user(user)
        return api_response.get_success_response("", [user_access_control.control_id for
                                                      user_access_control in user_access_controls])
    except Exception as e:
        return api_response.get_error_response("An error has occurred", str(e), 400)


@access_bp.route('/can_access', methods=['GET'])
@authenticate_token_access_or_self(constants.ACCOUNT_ACCESS_CONTROL_ID, constants.EDIT_ALL_USERS_ACCESS_CONTROL_ID,
                                   constants.VIEW_ALL_USERS_ACCESS_CONTROL_ID)
def can_user_access():
    global api_method
    api_method = "CAN_ACCESS"

    user = request.args.get('username')
    control_id = request.args.get('control_id')

    try:
        return api_response.get_success_response("", user_access_service.can_access(user, control_id))
    except Exception as e:
        return api_response.get_error_response("An error has occurred", str(e), 400)
