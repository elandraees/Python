from flask import jsonify
import json


def get_success_response(message, result):
    return jsonify({"success": True, "message": message, "result": result}), 200


def get_error_response(message, result, code):
    return jsonify({"success": False, "message": message, "result": result}), code
