from glob import glob
import os

HERE = os.path.abspath(os.path.dirname(__file__))

templates = os.path.join(HERE, "templates")

config = {
    "add": {
        "MYSQL_PASSWORD": "{{ 8|random_string }}",
        "SECRET_KEY": "{{ 20|random_string }}",
        "OAUTH2_SECRET": "{{ 8|random_string }}",
    },
    "defaults": {
        "DOCKER_IMAGE": "overhangio/openedx-discovery:{{ TUTOR_VERSION }}",
        "HOST": "discovery.{{ LMS_HOST }}",
        "INDEX_NAME": "catalog",
        "MYSQL_DATABASE": "discovery",
        "MYSQL_USERNAME": "discovery",
        "MYSQL_USERNAME": "discovery",
        "OAUTH2_KEY": "discovery",
    },
}

hooks = {
    "build-image": {"discovery": "{{ DISCOVERY_DOCKER_IMAGE }}"},
    "remote-image": {"discovery": "{{ DISCOVERY_DOCKER_IMAGE }}"},
    "init": ["mysql-client", "lms", "discovery"],
}


def patches():
    all_patches = {}
    for path in glob(os.path.join(HERE, "patches", "*")):
        with open(path) as patch_file:
            name = os.path.basename(path)
            content = patch_file.read()
            all_patches[name] = content
    return all_patches
