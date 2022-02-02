import json
import time
import requests
import os
import base64
from flask import request, Response, current_app

class PreAuthorize:

    USER_ROLES = {}

    @classmethod
    def is_preauthorize_enabled(cls):
        return current_app.config.get("flask_c8y_pre_authorize_enabled", True)

    @classmethod
    def cache_timeout(cls):
        return current_app.config.get("flask_c8y_user_roles_cache_timeout", 10)

    @classmethod
    def has_any_role(cls, roles):
        def wrapper(func):
            def inner(*args, **kwargs):
                if cls.is_preauthorize_enabled():
                    user_roles = cls.__get_current_user_roles()
                    if not user_roles or len(set(roles).intersection(set(user_roles)))==0:
                        return cls.__access_denied()
                return func(*args, **kwargs)
            inner.__name__ = func.__name__
            return inner
        return wrapper

    @classmethod
    def has_role(cls, role):
        def wrapper(func):
            def inner(*args, **kwargs):
                if cls.is_preauthorize_enabled():
                    user_roles = cls.__get_current_user_roles()
                    if not user_roles or role not in user_roles:
                        return cls.__access_denied()
                return func(*args, **kwargs)
            inner.__name__ = func.__name__
            return inner
        return wrapper

    @classmethod
    def has_all_roles(cls, roles):
        def wrapper(func):
            def inner(*args, **kwargs):
                if cls.is_preauthorize_enabled():
                    user_roles = cls.__get_current_user_roles()
                    if not user_roles or len(set(roles) - set(user_roles)) > 0:
                        return cls.__access_denied()
                return func(*args, **kwargs)
            inner.__name__ = func.__name__
            return inner
        return wrapper

    @classmethod
    def __get_user(cls, auth_header):
        # Handles basic auth
        auth = auth_header.split(" ")[-1]
        username, password = base64.b64decode(auth).decode().split(":")
        user = username.split("/", 1)[-1]
        return user

    @classmethod
    def __get_current_user_roles(cls):
        auth = request.headers.get("Authorization")
        if not auth:
            return
        headers = {"Authorization": auth}
        user = cls.__get_user(auth)
        if (user not in cls.USER_ROLES) or \
                (user in cls.USER_ROLES and (time.time()-cls.USER_ROLES[user]["lastAccessed"]) >= cls.cache_timeout()):
            user_info_url = "{}/user/currentUser".format(os.getenv("C8Y_BASEURL"))
            user_info = requests.get(user_info_url, headers=headers)
            if user_info.status_code != 200:
                return
            user_roles = []
            for role in user_info.json()["effectiveRoles"]:
                user_roles.append(role["name"])
            cls.USER_ROLES[user] = {"roles": user_roles, "lastAccessed": time.time()}
        else:
            user_roles = cls.USER_ROLES[user]["roles"]
        return user_roles

    @classmethod
    def __access_denied(cls):
        resp = Response()
        resp.status_code = 403
        resp.set_data(json.dumps({"error": "Access is denied"}))
        resp.content_type = "application/json"
        return resp