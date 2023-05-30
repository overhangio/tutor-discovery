from __future__ import annotations

from glob import glob
import os
import pkg_resources
import typing as t

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
        "EXTRA_PIP_REQUIREMENTS": [],
    },
}

# Initialization tasks
init_tasks = ("mysql", "lms", "discovery")
for service in init_tasks:
    with open(
        os.path.join(
            pkg_resources.resource_filename("tutordiscovery", "templates"),
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


@tutor_hooks.Filters.APP_PUBLIC_HOSTS.add()
def _print_discovery_public_hosts(hosts: list[str], context_name: t.Literal["local", "dev"]) -> list[str]:
    if context_name == "dev":
        # todo: will may change the below dev port when i try this plugin in dev mode
        hosts += ["discovery.{{ LMS_HOST }}:8381"]
    else:
        hosts += ["discovery.{{ LMS_HOST }}"]
    return hosts


REPO_PREFIX = "frontend-app-"


@tutor_hooks.Filters.COMPOSE_MOUNTS.add()
def _mount_frontend_apps(volumes, path_basename):
    """
    If the user mounts any repo named frontend-app-APPNAME, then make sure
    it's available in the APPNAME service container. This is only applicable
    in dev mode, because in production, all MFEs are built and hosted on the
    singular 'mfe' service container.
    """
    if path_basename.startswith(REPO_PREFIX):
        # Assumption:
        # For each repo named frontend-app-APPNAME, there is an associated
        # docker-compose service named APPNAME. If this assumption is broken,
        # then Tutor will try to mount the repo in a service that doesn't exist.
        app_name = path_basename[len(REPO_PREFIX) :]
        volumes += [(app_name, "/openedx/app")]
    return volumes


@tutor_hooks.Filters.IMAGES_BUILD_MOUNTS.add()
def _mount_frontend_apps_on_build(mounts: list[tuple[str, str]], host_path: str) -> list[tuple[str, str]]:
    path_basename = os.path.basename(host_path)
    if path_basename.startswith(REPO_PREFIX):
        # Bind-mount repo at build-time, both for prod and dev images
        app_name = path_basename[len(REPO_PREFIX) :]
        mounts.append(("mfe", f"{app_name}-src"))
        mounts.append((f"{app_name}-dev", f"{app_name}-src"))
    return mounts
