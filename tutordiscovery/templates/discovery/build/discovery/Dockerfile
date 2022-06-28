FROM docker.io/ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive
RUN apt update && \
  apt install -y curl git-core language-pack-en python3 python3-pip python3-venv \
  build-essential libffi-dev libmysqlclient-dev libxml2-dev libxslt-dev libjpeg-dev libssl-dev
ENV LC_ALL en_US.UTF-8

ARG APP_USER_ID=1000
RUN useradd --home-dir /openedx --create-home --shell /bin/bash --uid ${APP_USER_ID} app
USER ${APP_USER_ID}

ARG DISCOVERY_REPOSITORY=https://github.com/edx/course-discovery.git
ARG DISCOVERY_VERSION={{ OPENEDX_COMMON_VERSION }}
RUN mkdir -p /openedx/discovery && \
    git clone $DISCOVERY_REPOSITORY --branch $DISCOVERY_VERSION --depth 1 /openedx/discovery
WORKDIR /openedx/discovery

# Setup empty yml config file, which is required by production settings
RUN echo "{}" > /openedx/config.yml
ENV DISCOVERY_CFG /openedx/config.yml

# Install python venv
RUN python3 -m venv ../venv/
ENV PATH "/openedx/venv/bin:$PATH"
# https://pypi.org/project/setuptools/
# https://pypi.org/project/pip/
# https://pypi.org/project/wheel/
RUN pip install setuptools==62.1.0 pip==22.0.4 wheel==0.37.1

# Install a recent version of nodejs
RUN pip install nodeenv
# nodejs version picked from https://github.com/openedx/course-discovery/blob/master/Dockerfile
RUN nodeenv /openedx/nodeenv --node=16.14.2 --prebuilt
ENV PATH /openedx/nodeenv/bin:${PATH}

# Install python and nodejs requirements
# This is identical to "make production-requirements" but it was split in multiple
# instructions to benefit from docker image caching
RUN pip install -r requirements.txt
ARG NPM_REGISTRY=https://registry.npmjs.org/
RUN npm install --verbose --registry=$NPM_REGISTRY --production
RUN ./node_modules/.bin/bower install --allow-root --production

# Install django-redis for using redis as a django cache
# https://pypi.org/project/django-redis/
RUN pip install django-redis==5.2.0

# Install uwsgi
# https://pypi.org/project/uWSGI/
RUN pip install uwsgi==2.0.20

# Collect static assets
COPY --chown=app:app assets.py ./course_discovery/settings/assets.py
RUN DJANGO_SETTINGS_MODULE=course_discovery.settings.assets make static

# Run production server
ENV DJANGO_SETTINGS_MODULE course_discovery.settings.tutor.production
EXPOSE 8000
CMD uwsgi \
    --static-map /static=/openedx/discovery/course_discovery/assets \
    --static-map /media=/openedx/discovery/course_discovery/media \
    --http 0.0.0.0:8000 \
    --thunder-lock \
    --single-interpreter \
    --enable-threads \
    --processes=2 \
    --buffer-size=8192 \
    --wsgi-file course_discovery/wsgi.py
