import datetime
import util.date_util as date_util
from dataclasses import dataclass
import util.constants as constants


@dataclass
class UserAccessControl:
    control_id: int
    user_id: int
    account_id: int
    status_id: int = constants.MODEL_STATUS_ACTIVE
    create_date: datetime = date_util.now()
    last_update: datetime = date_util.now()
    id: int = 0

