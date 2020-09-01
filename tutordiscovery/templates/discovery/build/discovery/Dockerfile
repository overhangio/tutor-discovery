FROM docker.io/ubuntu:16.04

RUN apt update && \
  apt install -y curl git-core language-pack-en python3 python3-pip python3-venv \
  build-essential libffi-dev libmysqlclient-dev libxml2-dev libxslt-dev libjpeg-dev libssl-dev
ENV LC_ALL en_US.UTF-8

ARG DISCOVERY_REPOSITORY=https://github.com/edx/course-discovery.git
ARG DISCOVERY_VERSION=open-release/juniper.3
RUN mkdir -p /openedx/discovery && \
    git clone $DISCOVERY_REPOSITORY --branch $DISCOVERY_VERSION --depth 1 /openedx/discovery
WORKDIR /openedx/discovery

# Fix LMS read timeout
# https://github.com/edx/course-discovery/pull/2638
RUN curl https://github.com/overhangio/course-discovery/commit/733e9d889f5aa83a49f5192f74df11ea5b77add8.patch | git apply -

# Setup minimal yml config file, which is required by production settings
COPY config.yml /openedx/config.yml
ENV DISCOVERY_CFG /openedx/config.yml

# Install python venv
RUN python3 -m venv ../venv/
ENV PATH "/openedx/venv/bin:$PATH"
RUN pip install setuptools==44.1.0 pip==20.0.2 wheel==0.34.2

# Install a recent version of nodejs
RUN pip install nodeenv
RUN nodeenv /openedx/nodeenv --node=12.13.0 --prebuilt
ENV PATH /openedx/nodeenv/bin:${PATH}

# Install whitenoise for serving static assets
RUN pip install "whitenoise==5.1.0"

# Install python and nodejs requirements
# This is identical to "make production-requirements" but it was split in multiple
# instructions to benefit from docker image caching
RUN pip install -r requirements.txt
ARG NPM_REGISTRY=https://registry.npmjs.org/
RUN npm install --verbose --registry=$NPM_REGISTRY --production
RUN ./node_modules/.bin/bower install --allow-root --production

# Collect static assets
COPY assets.py ./course_discovery/settings/assets.py
ENV DJANGO_SETTINGS_MODULE course_discovery.settings.assets
RUN make static

EXPOSE 8000
CMD gunicorn --bind=0.0.0.0:8000 --workers 2 --max-requests=1000 course_discovery.wsgi:application
