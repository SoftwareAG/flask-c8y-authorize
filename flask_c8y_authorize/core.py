import json
import requests
import os
from flask import request, Response

class PreAuthorize:

    @classmethod
    def has_any_role(cls, roles):
        def wrapper(func):
            def inner(*args, **kwargs):
                user_roles = cls.__get_current_user_roles()
                if len(set(roles).intersection(set(user_roles)))==0:
                    return cls.__create_response(
                        status_code=403,
                        content_type="application/json",
                        message=json.dumps({"error": "You do not have any of the roles - {}.".format(roles)})
                    )
                return func(*args, **kwargs)
            inner.__name__ = func.__name__
            return inner
        return wrapper

    @classmethod
    def has_role(cls, role):
        def wrapper(func):
            def inner(*args, **kwargs):
                user_roles = cls.__get_current_user_roles()
                if role not in user_roles:
                    return cls.__create_response(
                        status_code=403,
                        content_type="application/json",
                        message=json.dumps({"error": "You do not have the role - {}.".format(role)})
                    )
                return func(*args, **kwargs)
            inner.__name__ = func.__name__
            return inner
        return wrapper

    @classmethod
    def has_all_roles(cls, roles):
        def wrapper(func):
            def inner(*args, **kwargs):
                user_roles = cls.__get_current_user_roles()
                if len(set(roles) - set(user_roles)) > 0:
                    return cls.__create_response(
                        status_code=403,
                        content_type="application/json",
                        message=json.dumps({"error": "You do not have all the roles - {}.".format(roles)})
                    )
                return func(*args, **kwargs)
            inner.__name__ = func.__name__
            return inner
        return wrapper

    @classmethod
    def __get_current_user_roles(cls):
        headers = {"Authorization": request.headers.get("Authorization")}
        user_info_url = "{}/user/currentUser".format(os.getenv("C8Y_BASEURL"))
        user_info = requests.get(user_info_url, headers=headers).json()
        user_roles = []
        for role in user_info["effectiveRoles"]:
            user_roles.append(role["name"])
        return user_roles

    @classmethod
    def __create_response(cls, status_code, content_type, message):
        resp = Response()
        resp.status_code = status_code
        resp.set_data(message)
        resp.content_type = content_type
        return resp