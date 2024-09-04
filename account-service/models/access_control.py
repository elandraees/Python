import datetime
import util.date_util as date_util
from dataclasses import dataclass
import services.access_service as access_service
import util.constants as constants
import util.validation_util as validation_util


@dataclass
class AccessControl:
    control_id: int
    name: str
    description: str
    control_type_id: int = 0
    control_level_id: int = 0
    status_id: int = constants.MODEL_STATUS_ACTIVE
    create_date: datetime = date_util.now()
    last_update: datetime = date_util.now()

    def validate(self, is_update):
        error_dict = {}

        if validation_util.is_none_empty_or_zero(self.control_id):
            error_dict["control_id"] = "Please specify the control id"

        if validation_util.is_none_empty_or_zero(self.name):
            error_dict["name"] = "Please specify the name"

        if (validation_util.is_none_empty_or_zero(self.description)) or len(self.description) < 10:
            error_dict["description"] = "Please give a short description of this control"

        if self.status_id < 0:
            error_dict["status"] = "Please specify a valid status"

        if is_update:
            return error_dict

        try:
            self.__check_duplicate()
        except Exception as e:
            error_dict["duplicate_control"] = str(e)

        return error_dict

    def __check_duplicate(self):
        access_control = access_service.get_access_control(self.control_id)
        if access_control:
            raise Exception("Control exists.")

    def to_json(self):
        return {
            "control_id": self.control_id,
            "name": self.name,
            "description": self.description,
            "status": constants.MODEL_STATUS_MAP_ID[self.status_id]
        }

