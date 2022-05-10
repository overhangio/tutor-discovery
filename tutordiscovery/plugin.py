from glob import glob
import os
import pkg_resources

from tutor import hooks as tutor_hooks

from .__about__ import __version__

HERE = os.path.abspath(os.path.dirname(__file__))


config = {
    "unique": {
        "MYSQL_PASSWORD": "{{ 8|random_string }}",
        "SECRET_KEY": "{{ 20|random_string }}",
        "OAUTH2_SECRET": "{{ 8|random_string }}",
        "OAUTH2_SECRET_SSO": "{{ 8|random_string }}",
    },
    "defaults": {
        "VERSION": __version__,
        "DOCKER_IMAGE": "{{ DOCKER_REGISTRY}}overhangio/openedx-discovery:{{ DISCOVERY_VERSION }}",
        "HOST": "discovery.{{ LMS_HOST }}",
        "INDEX_OVERRIDES": {},
        "MYSQL_DATABASE": "discovery",
        "MYSQL_USERNAME": "discovery",
        "OAUTH2_KEY": "discovery",
        "OAUTH2_KEY_DEV": "discovery-dev",
        "OAUTH2_KEY_SSO": "discovery-sso",
        "OAUTH2_KEY_SSO_DEV": "discovery-sso-dev",
        "CACHE_REDIS_DB": "{{ OPENEDX_CACHE_REDIS_DB }}",
    },
}

# Initialization tasks
tutor_hooks.Filters.COMMANDS_INIT.add_item(
    (
        "mysql",
        ("discovery", "tasks", "mysql", "init"),
    )
)
tutor_hooks.Filters.COMMANDS_INIT.add_item(
    (
        "lms",
        ("discovery", "tasks", "lms", "init"),
    )
)
tutor_hooks.Filters.COMMANDS_INIT.add_item(
    (
        "discovery",
        ("discovery", "tasks", "discovery", "init"),
    )
)

# Image management
tutor_hooks.Filters.IMAGES_BUILD.add_item(
    (
        "discovery",
        ("plugins", "discovery", "build", "discovery"),
        "{{ DISCOVERY_DOCKER_IMAGE }}",
        (),
    )
)
tutor_hooks.Filters.IMAGES_PULL.add_item(
    (
        "discovery",
        "{{ DISCOVERY_DOCKER_IMAGE }}",
    )
)
tutor_hooks.Filters.IMAGES_PUSH.add_item(
    (
        "discovery",
        "{{ DISCOVERY_DOCKER_IMAGE }}",
    )
)

# Automount /openedx/discovery folder from the container
@tutor_hooks.Filters.COMPOSE_MOUNTS.add()
def _mount_course_discovery(mounts, name):
    if name == "course-discovery":
        mounts.append(("discovery", "/openedx/discovery"))
    return mounts


####### Boilerplate code
# Add the "templates" folder as a template root
tutor_hooks.Filters.ENV_TEMPLATE_ROOTS.add_item(
    pkg_resources.resource_filename("tutordiscovery", "templates")
)
# Render the "build" and "apps" folders
tutor_hooks.Filters.ENV_TEMPLATE_TARGETS.add_items(
    [
        ("discovery/build", "plugins"),
        ("discovery/apps", "plugins"),
    ],
)
# Load patches from files
for path in glob(
    os.path.join(
        pkg_resources.resource_filename("tutordiscovery", "patches"),
        "*",
    )
):
    with open(path, encoding="utf-8") as patch_file:
        tutor_hooks.Filters.ENV_PATCHES.add_item(
            (os.path.basename(path), patch_file.read())
        )
# Add configuration entries
tutor_hooks.Filters.CONFIG_DEFAULTS.add_items(
    [(f"DISCOVERY_{key}", value) for key, value in config.get("defaults", {}).items()]
)
tutor_hooks.Filters.CONFIG_UNIQUE.add_items(
    [(f"DISCOVERY_{key}", value) for key, value in config.get("unique", {}).items()]
)
tutor_hooks.Filters.CONFIG_OVERRIDES.add_items(
    list(config.get("overrides", {}).items())
)
