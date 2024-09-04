from models.access_control import AccessControl
import util.json_util as json_util
import repositories.access_control_repo as access_control_repo


def create_access_control(json) -> AccessControl:
    access_control: AccessControl = __get_access_control_from_json(json)

    errors = access_control.validate(False)
    print(errors)

    if errors:
        raise Exception(errors)

    access_control_repo.create_access_control(access_control)

    return access_control


def get_access_control(control_id) -> AccessControl:
    return access_control_repo.get_control(control_id)


def get_controls(control_ids) -> [AccessControl]:
    access_controls: [AccessControl] = []
    for control_id in control_ids:
        access_control: AccessControl = get_access_control(control_id)
        if access_control is None:
            raise Exception('No control found for id: ' + str(control_id))
        else:
            access_controls.append(access_control)
    return access_controls


def __get_access_control_from_json(json) -> AccessControl:
    control_id = json_util.parse_json(json, 'control_id')
    name = json_util.parse_json(json, 'name')
    description = json_util.parse_json(json, 'description')

    return AccessControl(control_id, name, description)



