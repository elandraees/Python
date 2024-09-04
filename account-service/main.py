from flask import Flask, request, jsonify
from controllers.v1.account_controller import account_bp
from controllers.v1.user_controller import user_bp
from controllers.v1.access_controller import access_bp
from flask_cors import CORS, cross_origin

app = Flask(__name__)

app.register_blueprint(account_bp)
app.register_blueprint(user_bp)
app.register_blueprint(access_bp)


# Local deployment:
# If debug is disabled, the development server on the local computer can be made available to
# users on the network by setting the host name to ‘0.0.0.0’.
if __name__ == '__main__':
    app.run(debug=True, port=5001)


'''
Endpoint details:

local base url: http://127.0.0.1:5001/accounts/v1

Account Endpoints
/
/update
/authenticate
/list
/create

User Endpoints
/user/update
/user
/users
/user/create

Access Endpoints
/access/create
/access/can_access
/access/get_access
/access/remove
/access/update
'''
