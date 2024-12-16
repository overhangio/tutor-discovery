from __future__ import annotations

import os
import typing as t
from glob import glob

import importlib_resources
from tutor import hooks as tutor_hooks
from tutor.__about__ import __version_suffix__

from .__about__ import __version__
from .utils import is_docker_rootless

# Handle version suffix in main mode, just like tutor core
if __version_suffix__:
    __version__ += "-" + __version_suffix__

HERE = os.path.abspath(os.path.dirname(__file__))
REPO_NAME = "course-discovery"
APP_NAME = "discovery"

config: t.Dict[str, t.Dict[str, t.Any]] = {
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
        "ATLAS_PULL": False,
        "DEFAULT_PRODUCT_SOURCE_SLUG": "edx",
        "EXTRA_PIP_REQUIREMENTS": [],
        "REPOSITORY": "https://github.com/openedx/course-discovery.git",
        "REPOSITORY_VERSION": "{{ OPENEDX_COMMON_VERSION }}",
        "RUN_ELASTICSEARCH": True,
        "DOCKER_IMAGE_ELASTICSEARCH": "docker.io/elasticsearch:7.17.13",
        "ELASTICSEARCH_HOST": "elasticsearch",
        "ELASTICSEARCH_PORT": 9200,
        "ELASTICSEARCH_SCHEME": "http",
        "ELASTICSEARCH_HEAP_SIZE": "1g",
    },
    "unique": {
        "MYSQL_PASSWORD": "{{ 8|random_string }}",
        "SECRET_KEY": "{{ 20|random_string }}",
        "OAUTH2_SECRET": "{{ 8|random_string }}",
        "OAUTH2_SECRET_SSO": "{{ 8|random_string }}",
    },
}

# Initialization tasks
init_tasks = ("mysql", "lms", "discovery")
for service in init_tasks:
    with open(
        os.path.join(
            str(importlib_resources.files("tutordiscovery") / "templates"),
            "discovery",
            "tasks",
            service,
            "init",
        ),
        encoding="utf8",
    ) as fi:
        tutor_hooks.Filters.CLI_DO_INIT_TASKS.add_item(
            (
                service,
                fi.read(),
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
def _mount_course_discovery(
    mounts: list[tuple[str, str]], name: str
) -> list[tuple[str, str]]:
    if name == REPO_NAME:
        mounts.append((APP_NAME, "/openedx/discovery"))
    return mounts


# Bind-mount repo at build-time, both for prod and dev images
@tutor_hooks.Filters.IMAGES_BUILD_MOUNTS.add()
def _mount_course_discovery_on_build(
    mounts: list[tuple[str, str]], host_path: str
) -> list[tuple[str, str]]:
    path_basename = os.path.basename(host_path)
    if path_basename == REPO_NAME:
        mounts.append((APP_NAME, f"{APP_NAME}-src"))
        mounts.append((f"{APP_NAME}-dev", f"{APP_NAME}-src"))
    return mounts


# Add the "templates" folder as a template root
tutor_hooks.Filters.ENV_TEMPLATE_ROOTS.add_item(
    str(importlib_resources.files("tutordiscovery") / "templates")
)
# Render the "build" and "apps" folders
tutor_hooks.Filters.ENV_TEMPLATE_TARGETS.add_items(
    [
        ("discovery/build", "plugins"),
        ("discovery/apps", "plugins"),
    ],
)
# Template variables
tutor_hooks.Filters.ENV_TEMPLATE_VARIABLES.add_item(
    ("is_docker_rootless", is_docker_rootless),
)
# Load patches from files
for path in glob(
    os.path.join(
        str(importlib_resources.files("tutordiscovery") / "patches"),
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


@tutor_hooks.Filters.APP_PUBLIC_HOSTS.add()
def _print_discovery_public_hosts(
    hosts: list[str], context_name: t.Literal["local", "dev"]
) -> list[str]:
    if context_name == "dev":
        hosts += ["{{ DISCOVERY_HOST }}:8381"]
    else:
        hosts += ["{{ DISCOVERY_HOST }}"]
    return hosts
