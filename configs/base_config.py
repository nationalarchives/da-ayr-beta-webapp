import os


class Config(object):
    RATELIMIT_HEADERS_ENABLED = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = True

    APP_BASE_URL = os.getenv("APP_BASE_URL", "")
    CONTACT_EMAIL = os.getenv("CONTACT_EMAIL", "")
    CONTACT_PHONE = os.getenv("CONTACT_PHONE", "")
    DEPARTMENT_NAME = os.getenv("DEPARTMENT_NAME", "")
    DEPARTMENT_URL = os.getenv("DEPARTMENT_URL", "")
    RATELIMIT_STORAGE_URI = os.getenv("RATELIMIT_STORAGE_URI", "")
    SECRET_KEY = os.getenv("SECRET_KEY", "")
    SERVICE_NAME = os.getenv("SERVICE_NAME", "")
    SERVICE_PHASE = os.getenv("SERVICE_PHASE", "")
    SERVICE_URL = os.getenv("SERVICE_URL", "")
    AWS_REGION = os.getenv("AWS_REGION", "")
    AWS_OPEN_SEARCH_INDEX = os.getenv("AWS_OPEN_SEARCH_INDEX", "")
    AWS_OPEN_SEARCH_USERNAME = os.getenv("AWS_OPEN_SEARCH_HOST", "")
    AWS_OPEN_SEARCH_PASSWORD = os.getenv("AWS_OPEN_SEARCH_PASSWORD", "")
    AWS_OPEN_SEARCH_USERNAME = os.getenv("AWS_OPEN_SEARCH_USERNAME", "")
    KEYCLOAK_BASE_URI = os.getenv("KEYCLOAK_BASE_URI", "")
    KEYCLOAK_CLIENT_ID = os.getenv("KEYCLOAK_CLIENT_ID", "")
    KEYCLOAK_REALM_NAME = os.getenv("KEYCLOAK_REALM_NAME", "")
    KEYCLOAK_CLIENT_SECRET = os.getenv("KEYCLOAK_CLIENT_SECRET", "")
    KEYCLOAK_AYR_USER_GROUP = os.getenv("KEYCLOAK_AYR_USER_GROUP", "")
