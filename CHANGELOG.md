# Changelog

This file includes a history of past releases. Changes that were not yet added to a release are in the [changelog.d/](./changelog.d) folder.

<!--
⚠️ DO NOT ADD YOUR CHANGES TO THIS FILE! (unless you want to modify existing changelog entries in this file)
Changelog entries are managed by scriv. After you have made some changes to this plugin, create a changelog entry with:

    scriv create

Edit and commit the newly-created file in changelog.d.

If you need to create a new release, create a separate commit just for that. It is important to respect these
instructions, because git commits are used to generate release notes:
  - Modify the version number in `__about__.py`.
  - Collect changelog entries with `scriv collect`
  - The title of the commit should be the same as the new version: "vX.Y.Z".
-->

<!-- scriv-insert-here -->

<a id='changelog-21.0.1'></a>
## v21.0.1 (2026-01-28)

- [Chore] Remove unnecessary hatch definition for version. (by @mlabeeb03)

- [BugFix] Add correct EVENT_BUS_REDIS_CONNECTION_URL settings for event-bus. (by @Faraz32123)

- [Bugfix] Add CELERY_BROKER_URL settings as celery tasks were failing due to empty celery broker url. (by @Faraz32123)

- [Bugfix] Fix site configuration initialization by ensuring all sites have names before running create_or_update_site_configuration to prevent IntegrityError (by @CodeWithEmad)

<a id='changelog-21.0.0'></a>
## v21.0.0 (2025-10-01)

- [Improvement] Migrate from pylint and black to ruff. (by @mlabeeb03)
- [Improvement] Test python package distribution build when running make test. (by @mlabeeb03)

- 💥[Feature] Upgrade to Ulmo. (by @mlabeeb03)

<a id='changelog-20.0.0'></a>
## v20.0.0 (2025-06-05)

- [Bugfix] Add support to consume events from event bus in discovery. Explanation can be viewed here: https://github.com/openedx/event-bus-redis/blob/main/docs/tutor_installation.rst. (by @Faraz32123)

- [Feature] Introduced a new environment variable to enable or disable programs. (by @Faraz32123)
  - This aligns with the frontend, which now also utilizes this environment variable. To view the frontend related changes, click here: https://github.com/openedx/frontend-app-learner-dashboard/pull/506/files.
  - Additionally, it automates the enabling of programs in the "programapiconfig" model on the LMS admin panel through init tasks.

- [Improvement] Migrate packaging from setup.py/setuptools to pyproject.toml/hatch. (by @Faraz32123)
  - For more details view tutor core PR: https://github.com/overhangio/tutor/pull/1163

- [Improvement] Add hatch_build.py in sdist target to fix the installation issues (by @dawoudsheraz)

- [Improvement] Replace site-configuration script with create_or_update_site_configuration management command in the init task. (by @Danyal-Faheem)

- 💥[Feature] Upgrade to Teak. (by @mlabeeb03)

<a id='changelog-19.0.0'></a>
## v19.0.0 (2024-10-23)

- 💥[Feature] Upgrade to Sumac. (by @Faraz32123)
- [Feature] Add Elasticsearch support in tutor-discovery. As Tutor and Open edX have shifted to Meilisearch, and course-discovery still depends on Elasticsearch, running the Elasticsearch container with tutor-discovery will facilitate smoother operation for the course-discovery service. (by @Faraz32123)
  - Please see related tutor core PR for context https://github.com/overhangio/tutor/pull/1141
- 💥 [Deprecation] Drop support for python 3.8 and set Python 3.9 as the minimum supported python version. (by @Faraz32123)
- 💥[Improvement] Rename Tutor's two branches (by @DawoudSheraz):
  * Rename **master** to **release**, as this branch runs the latest official Open edX release tag.
  * Rename **nightly** to **main**, as this branch runs the Open edX master branches, which are the basis for the next Open edX release.
- [Improvement] Move is_docker_rootless method related to elasticsearch from tutor core to tutor-discovery. (by @Faraz32123)
- 💥[Feature] Update Course Discovery Image to use Ubuntu 22.04 as base OS. (by @hinakhadim)
- [Bugfix] Fix catalog_service_user permissions and 403 while fetching pathways (by @dyudyunov)
- [BugFix] Fix images(media) persistance issue by mounting media directory in volumes through patches. (by @Faraz32123)
- [Bugfix] Fix legacy warnings during Docker build. (by @regisb)


<a id='changelog-18.0.0'></a>
## v18.0.0 (2024-05-14)

- 💥[Feature] Upgrade to Redwood. (by @Faraz32123)
- 💥[Feature] Upgrade Python version to 3.12.2. (by @Faraz32123)
- [BugFix] Fix wrong mime type by adding mime-support dependency. (by @Faraz32123)

<a id='changelog-17.0.1'></a>
## v17.0.1 (2024-04-25)

- [Bugfix] Make plugin compatible with Python 3.12 by removing dependency on `pkg_resources`. (by @regisb)
- [Feature] Make it possible to use mounts for a local development. (by @cmltawt0)
- [Bugfix] Fix volumes empty list error during tutor dev launch. (by @Faraz32123)
- [Bugfix] Fix the docker image to allow media files to be served by uwsgi. (by @angonz)

<a id='changelog-17.0.0'></a>
## v17.0.0 (2023-12-09)

- 💥 [Feature] Upgrade to Quince. (by @ziafazal)
- [Bugfix] Fix missing pkg-config during image build. (by @regisb)
- [Feature] Pull translations via `atlas` during Docker build. (by @OmarIthawi)

<a id='changelog-16.0.2'></a>
## v16.0.2 (2023-12-09)

- [Improvement] Added Typing to code, Makefile and test action to the repository and formatted code with Black and isort. (by @CodeWithEmad)
- [Improvement] Introduced Course Discovery Repository and Version settings. (by @Faraz32123)
- [BugFix] Fix base url for discovery media files, including program banner images. (by @Faraz32123)

<a id='changelog-16.0.1'></a>
## v16.0.1 (2023-11-08)

- [Improvement] Add a scriv-compliant changelog. (by @regisb)
- [BugFix] Corrected variable name for installing extra pip requirements. (by @Faraz32123)

