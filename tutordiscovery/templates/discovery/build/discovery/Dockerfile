# syntax=docker/dockerfile:1.4
###### Minimal image with base system requirements for most stages
FROM docker.io/ubuntu:22.04 AS minimal

ENV DEBIAN_FRONTEND=noninteractive
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    apt update && \
    apt install -y curl git-core gettext language-pack-en \
    build-essential libcairo2 libffi-dev libmysqlclient-dev libxml2-dev libxslt-dev libjpeg-dev libssl-dev \
    pkg-config libsqlite3-dev media-types mailcap
ENV LC_ALL=en_US.UTF-8

ARG APP_USER_ID=1000
RUN if [ "$APP_USER_ID" = 0 ]; then echo "app user may not be root" && false; fi
RUN useradd --home-dir /openedx --create-home --shell /bin/bash --uid ${APP_USER_ID} app
USER ${APP_USER_ID}

###### Git-clone course-discovery repo
ARG DISCOVERY_REPOSITORY='{{ DISCOVERY_REPOSITORY }}'
ARG DISCOVERY_VERSION='{{ DISCOVERY_REPOSITORY_VERSION }}'
RUN mkdir -p /openedx/discovery && \
    git clone $DISCOVERY_REPOSITORY --branch $DISCOVERY_VERSION --depth 1 /openedx/discovery
WORKDIR /openedx/discovery

# Setup empty yml config file, which is required by production settings
RUN echo "{}" > /openedx/config.yml
ENV DISCOVERY_CFG=/openedx/config.yml

# Install pyenv
# https://www.python.org/downloads/
# https://github.com/pyenv/pyenv/releases
ARG PYTHON_VERSION=3.12.2
ENV PYENV_ROOT=/opt/pyenv
# root user is required for below 2 steps, as app user gets permission denied.
USER root
RUN git clone https://github.com/pyenv/pyenv $PYENV_ROOT --branch v2.3.36 --depth 1
# Install Python
RUN $PYENV_ROOT/bin/pyenv install $PYTHON_VERSION
USER app

# Create virtualenv
RUN $PYENV_ROOT/versions/$PYTHON_VERSION/bin/python -m venv /openedx/venv
ENV PATH=/openedx/venv/bin:$PATH

RUN --mount=type=cache,target=/openedx/.cache/pip,sharing=shared pip install \
    # https://pypi.org/project/setuptools/
    # https://pypi.org/project/pip/
    # https://pypi.org/project/wheel/
    setuptools==75.2.0 pip==24.2 wheel==0.44.0

# Install a recent version of nodejs
RUN pip install nodeenv==1.9.1
# nodejs version picked from https://github.com/openedx/course-discovery/blob/master/Dockerfile
RUN nodeenv /openedx/nodeenv --node=16.14.2 --prebuilt
ENV PATH=/openedx/nodeenv/bin:${PATH}

# Install python and nodejs requirements
# This is identical to "make production-requirements" but it was split in multiple
# instructions to benefit from docker image caching
# Install base requirements
RUN --mount=type=cache,target=/openedx/.cache/pip,sharing=shared pip install -r requirements.txt
{% for extra_requirement in DISCOVERY_EXTRA_PIP_REQUIREMENTS %}RUN --mount=type=cache,target=/openedx/.cache/pip,sharing=shared pip install '{{ extra_requirement }}'
{% endfor %}

# Install npm, bower requirements
ARG NPM_REGISTRY='{{ NPM_REGISTRY }}'
RUN --mount=type=cache,target=/openedx/.npm/,sharing=shared,uid=${APP_USER_ID} npm clean-install --verbose --no-audit --registry=$NPM_REGISTRY --production
RUN --mount=type=cache,target=/openedx/.cache/bower,sharing=shared,uid=${APP_USER_ID} ./node_modules/.bin/bower install --allow-root --production

# Install extra requirements
RUN --mount=type=cache,target=/openedx/.cache/pip,sharing=shared pip install \
    # Use redis as a django cache https://pypi.org/project/django-redis/
    django-redis==5.4.0 \
    # uwsgi server https://pypi.org/project/uWSGI/
    uwsgi==2.0.27

{% if DISCOVERY_ATLAS_PULL %}
# Pull translations. Support the OEP-58 proposal behind a feature flag until it's fully implemented.
RUN atlas pull {{ patch("atlas-extra-args") }} translations/course-discovery/course_discovery/conf/locale:course_discovery/conf/locale
RUN python manage.py compilemessages
{% endif %}

# Collect static assets
COPY --chown=app:app assets.py ./course_discovery/settings/assets.py
RUN DJANGO_SETTINGS_MODULE=course_discovery.settings.assets make static

# Create media directory to serve media files
RUN mkdir course_discovery/media

# Run production server
ENV DJANGO_SETTINGS_MODULE=course_discovery.settings.tutor.production
EXPOSE 8000
CMD ["uwsgi", \
    "--static-map", "/static=/openedx/discovery/course_discovery/assets", \
    "--static-map", "/media=/openedx/discovery/course_discovery/media", \
    "--http", "0.0.0.0:8000", \
    "--thunder-lock", \
    "--single-interpreter", \
    "--enable-threads", \
    "--processes=2", \
    "--buffer-size=8192", \
    "--wsgi-file", "course_discovery/wsgi.py"]
