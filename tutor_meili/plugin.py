from __future__ import annotations

import os
import typing as t
from glob import glob

import importlib_resources
from tutor import hooks as tutor_hooks
from tutor.__about__ import __version_suffix__

from .__about__ import __version__

# Handle version suffix in nightly mode, just like tutor core
if __version_suffix__:
    __version__ += "-" + __version_suffix__

HERE = os.path.abspath(os.path.dirname(__file__))

config: dict[str, dict[str, t.Any]] = {
    "defaults": {
        "VERSION": __version__,
        # use an index prefix to segregate data if you have multiple Open edX instances sharing one Meilisearch instance
        "INDEX_PREFIX": "tutor_",
        "PUBLIC_HOST": "meilisearch.{{ LMS_HOST }}",
        "DOCKER_IMAGE": "docker.io/getmeili/meilisearch:v1.6",
    },
    "unique": {
        # A key that can be used to generate other API keys:
        "MASTER_KEY": "{{ 24|random_string }}",
    },
    "overrides": {
        # Override other Tutor settings using the above values, if needed.
    },
}

# Add configuration entries
tutor_hooks.Filters.CONFIG_DEFAULTS.add_items(
    [(f"MEILISEARCH_{key}", value) for key, value in config.get("defaults", {}).items()]
)
tutor_hooks.Filters.CONFIG_UNIQUE.add_items(
    [(f"MEILISEARCH_{key}", value) for key, value in config.get("unique", {}).items()]
)
tutor_hooks.Filters.CONFIG_OVERRIDES.add_items(
    list(config.get("overrides", {}).items())
)


@tutor_hooks.Filters.APP_PUBLIC_HOSTS.add()
def add_meilisearch_hosts(
    hosts: list[str], context_name: t.Literal["local", "dev"]
) -> list[str]:
    if context_name == "dev":
        hosts.append("{{ MEILISEARCH_PUBLIC_HOST }}:7700")
    else:
        hosts.append("{{ MEILISEARCH_PUBLIC_HOST }}")
    return hosts


# Add pre-init script as init task with high priority
# with open(
#     os.path.join(HERE, "templates", "meilisearch", "tasks", "meilisearch", "init.sh"),
#     encoding="utf-8",
# ) as fi:
#     tutor_hooks.Filters.CLI_DO_INIT_TASKS.add_item(
#         ("meilisearch", fi.read()), priority=tutor_hooks.priorities.HIGH
#     )

# Add the "templates" folder as a template root
# tutor_hooks.Filters.ENV_TEMPLATE_ROOTS.add_item(
#     str(importlib_resources.files("tutor_meili") / "templates")
# )
# Render the "build" and "apps" folders
# tutor_hooks.Filters.ENV_TEMPLATE_TARGETS.add_items(
#     [
#         ("meilisearch/build", "plugins"),
#         ("meilisearch/apps", "plugins"),
#     ],
# )
# Load patches from files
for path in glob(str(importlib_resources.files("tutor_meili") / "patches" / "*")):
    with open(path, encoding="utf-8") as patch_file:
        tutor_hooks.Filters.ENV_PATCHES.add_item(
            (os.path.basename(path), patch_file.read())
        )
