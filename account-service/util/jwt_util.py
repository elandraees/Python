import jwt
import util.constants as constants
from datetime import datetime, timedelta


def get_decoded_token(request):
    header = request.headers.get(constants.AUTH_HEADER)
    token = ''
    if header is not None and header.startswith(constants.BEARER_AUTH_HEADER):
        token = header[7:]
    if not token:
        return None
    try:
        return jwt.decode(token, constants.SECRET_JWT_KEY, options={"verify_signature": False},
                          algorithms=[constants.JWT_ALGORITHM])
    except Exception as e:
        return None


def create_token(account_id, username, account_username) -> str:
    payload = {
        constants.JWT_PAYLOAD_ACCOUNT_ID: account_id,
        constants.JWT_PAYLOAD_ACCOUNT_USERNAME: account_username,
        constants.JWT_PAYLOAD_USERNAME: username,
        constants.JWT_PAYLOAD_EXP: datetime.utcnow() + timedelta(hours=2)  # Token will expire in 2 hour
    }
    token = jwt.encode(payload, constants.SECRET_JWT_KEY, algorithm=constants.JWT_ALGORITHM)
    return token
