from .production import *

SECRET_KEY = "{{ DISCOVERY_SECRET_KEY }}"
ALLOWED_HOSTS = ["localhost", "discovery.localhost", "{{ DISCOVERY_HOST }}"]
PLATFORM_NAME = "{{ PLATFORM_NAME }}"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "{{ DISCOVERY_MYSQL_DATABASE }}",
        "USER": "{{ DISCOVERY_MYSQL_USERNAME }}",
        "PASSWORD": "{{ DISCOVERY_MYSQL_PASSWORD }}",
        "HOST": "{{ MYSQL_HOST }}",
        "PORT": "{{ MYSQL_PORT }}",
    }
}

HAYSTACK_CONNECTIONS["default"].update(
    {
        "URL": "http://{{ ELASTICSEARCH_HOST }}:{{ ELASTICSEARCH_PORT }}",
        "INDEX_NAME": "{{ DISCOVERY_INDEX_NAME }}",
    }
)

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.memcached.MemcachedCache",
        "KEY_PREFIX": "discovery",
        "LOCATION": "{{ MEMCACHED_HOST }}:{{ MEMCACHED_PORT }}",
    }
}

LANGUAGE_CODE = "{{ LANGUAGE_CODE }}"
PARLER_DEFAULT_LANGUAGE_CODE = LANGUAGE_CODE
PARLER_LANGUAGES[1][0]["code"] = LANGUAGE_CODE
PARLER_LANGUAGES["default"]["fallbacks"] = [PARLER_DEFAULT_LANGUAGE_CODE]

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "{{ SMTP_HOST }}"
EMAIL_PORT = "{{ SMTP_PORT }}"
EMAIL_HOST_USER = "{{ SMTP_USERNAME }}"
EMAIL_HOST_PASSWORD = "{{ SMTP_PASSWORD }}"
EMAIL_USE_TLS = {{ SMTP_USE_TLS }}

LOGGING["handlers"]["local"] = {
    "class": "logging.handlers.WatchedFileHandler",
    "filename": "/var/log/discovery.log",
    "formatter": "standard",
}

JWT_AUTH["ISSUER"] = "{{ JWT_COMMON_ISSUER }}"
JWT_AUTH["AUDIENCE"] = "{{ JWT_COMMON_AUDIENCE }}"
JWT_AUTH["SECRET_KEY"] = "{{ JWT_COMMON_SECRET_KEY }}"
SOCIAL_AUTH_EDX_OIDC_KEY = "{{ DISCOVERY_OAUTH2_KEY }}"
SOCIAL_AUTH_EDX_OIDC_SECRET = "{{ DISCOVERY_OAUTH2_SECRET }}"
SOCIAL_AUTH_EDX_OIDC_URL_ROOT = "{% if ACTIVATE_HTTPS %}https{% else %}http{% endif %}://{{ LMS_HOST }}/oauth"
SOCIAL_AUTH_EDX_OIDC_ID_TOKEN_DECRYPTION_KEY = SOCIAL_AUTH_EDX_OIDC_SECRET
EDX_DRF_EXTENSIONS = {
    'OAUTH2_USER_INFO_URL': '{% if ACTIVATE_HTTPS %}https{% else %}http{% endif %}://{{ LMS_HOST }}/oauth2/user_info',
}

STATIC_ROOT = "/openedx/static"
COMPRESS_ENABLED = True
COMPRESS_OFFLINE = True
