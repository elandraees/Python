import util.validation_util as validation_util
import util.date_util as date_util
import util.constants as constants
from dataclasses import dataclass
import datetime
import repositories.user_repo as user_repo


@dataclass
class User:
    account_id: int
    first_name: str
    last_name: str
    username: str
    password: str
    email_address: str
    contact_number: str
    status_id: int
    user_type_id: int = constants.USER_TYPE_MAIN
    create_date: datetime = date_util.now()
    last_update: datetime = date_util.now()
    user_id: int = 0

    def update(self, user_data):
        self.first_name = self.first_name if validation_util.is_none_empty_or_zero(user_data.first_name) \
            else user_data.first_name

        self.last_name = self.last_name if validation_util.is_none_empty_or_zero(user_data.last_name) \
            else user_data.last_name

        self.password = self.password if validation_util.is_none_empty_or_zero(user_data.password) \
            else user_data.password

        self.email_address = self.email_address if validation_util.is_none_empty_or_zero(user_data.email_address) \
            else user_data.email_address

        self.contact_number = self.contact_number if validation_util.is_none_empty_or_zero(user_data.contact_number) \
            else user_data.contact_number

        self.status_id = self.status_id if validation_util.is_none_empty_or_zero(user_data.status_id) \
            else user_data.status_id

        self.last_update = date_util.now()

    def validate(self, is_update):
        error_dict = {}

        if self.account_id is None or self.account_id < 0:
            error_dict["account_id"] = "Please check account Id is a number greater than 0."

        if validation_util.is_none_empty_or_zero(self.first_name) or len(self.first_name) < 3:
            error_dict["first_name"] = "Please check the first name field is not empty and is greater " \
                                       "than 3 characters long."

        if validation_util.is_none_empty_or_zero(self.first_name) or len(self.first_name) < 3:
            error_dict["last_name"] = "Please check the last name field is not empty and is greater " \
                                      "than 3 characters long."

        # if validation_util.is_none_empty_or_zero(self.username) or len(self.username) < 5:
        #     error_dict["username"] = "Please check username field is not empty"

        if (validation_util.is_none_empty_or_zero(self.email_address)) \
                or (not validation_util.is_valid_email(self.email_address)):
            error_dict["email_address"] = "Please check email address field is not empty and is a valid email address."

        # if (validation_util.is_none_empty_or_zero(self.contact_number)) or (not self.contact_number.isnumeric()):
        #     error_dict["contact_number"] = "Please check cell number field is not empty and only contains numbers"

        if self.status_id < 0:
            error_dict["status"] = "Please specify a valid status."

        errors = validation_util.check_password(self.password)
        if len(errors) > 0:
            error_dict["password"] = '\n'.join(errors)

        if is_update:
            return error_dict

        try:
            self.__check_duplicate()
        except Exception as e:
            error_dict["duplicate_account"] = str(e)

        return error_dict

    def __check_duplicate(self):
        user = user_repo.get_user_by_username(self.username)

        if user:
            raise Exception("Account exists for username/email")

    def resolve_status(self):
        return constants.MODEL_STATUS_MAP_ID[self.status_id]

    def to_json(self):
        return {"first_name": self.first_name,
                "last_name": self.last_name,
                "username": self.username,
                "cell_number": self.contact_number, "email_address": self.email_address,
                "status": self.resolve_status(),
                "create_date": self.create_date, "last_update": self.last_update}

    def to_json_include_id(self):
        return {"user_id": self.user_id, "name": f'{self.first_name} {self.last_name}', "cell_number": self.contact_number,
                "email_address": self.email_address, "status": self.resolve_status(), "username": self.username,
                "create_date": self.create_date, "last_update": self.last_update}
