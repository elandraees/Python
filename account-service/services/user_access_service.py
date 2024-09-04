import services.user_service as user_service
from models.user import User
from models.user_access_control import UserAccessControl
import util.json_util as json_util
import repositories.user_access_control_repo as user_access_control_repo
import services.access_service as access_service
import util.constants as constants


def create_user_controls(json, username):
    user_controls: [UserAccessControl] = __get_new_user_controls(json, username)
    user_access_control_repo.create_user_access_controls(user_controls)


def remove_user_controls(json, username):
    user_controls: [UserAccessControl] = __get_existing_user_controls(json, username)
    user_access_control_repo.delete_user_access_controls(user_controls)


def get_user_control(user_id, control_id) -> UserAccessControl:
    return user_access_control_repo.get_control_for_user(user_id, control_id)


def get_all_controls_for_user(username) -> [UserAccessControl]:
    user: User = user_service.get_user(username)
    return user_access_control_repo.get_all_control_for_user(user.user_id)


def can_access(username, control_id) -> bool:
    user: User = user_service.get_user(username)

    # For now main user has super access
    if user.user_type_id == constants.USER_TYPE_MAIN:
        return True

    user_control: UserAccessControl = user_access_control_repo.get_control_for_user(user.user_id, control_id)
    return user_control is not None


def __get_new_user_controls(json, username) -> [UserAccessControl]:
    user: User = user_service.get_user(username)
    control_ids = json_util.parse_json(json, 'control_ids')

    if not isinstance(control_ids, list) or len(control_ids) == 0:
        raise Exception('Invalid control Ids specified, it must be a list of valid control Ids')

    user_access_controls: [UserAccessControl] = []
    for access_control in access_service.get_controls(control_ids):
        if not get_user_control(user.user_id, access_control.control_id):
            user_access_controls.append(UserAccessControl(access_control.control_id, user.user_id, user.account_id))

    return user_access_controls


def __get_existing_user_controls(json, username) -> [UserAccessControl]:
    user: User = user_service.get_user(username)
    control_ids = json_util.parse_json(json, 'control_ids')

    if not isinstance(control_ids, list) or len(control_ids) == 0:
        raise Exception('Invalid control Ids specified, it must be a list of valid control Ids')

    user_access_controls: [UserAccessControl] = []
    for access_control in access_service.get_controls(control_ids):
        if get_user_control(user.user_id, access_control.control_id):
            user_access_controls.append(UserAccessControl(access_control.control_id, user.user_id, user.account_id))

    return user_access_controls
