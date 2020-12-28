FROM docker.io/ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive
RUN apt update && \
  apt install -y curl git-core language-pack-en python3 python3-pip python3-venv \
  build-essential libffi-dev libmysqlclient-dev libxml2-dev libxslt-dev libjpeg-dev libssl-dev
ENV LC_ALL en_US.UTF-8

ARG DISCOVERY_REPOSITORY=https://github.com/edx/course-discovery.git
ARG DISCOVERY_VERSION={{ OPENEDX_COMMON_VERSION }}
RUN mkdir -p /openedx/discovery && \
    git clone $DISCOVERY_REPOSITORY --branch $DISCOVERY_VERSION --depth 1 /openedx/discovery
WORKDIR /openedx/discovery

# Fix TypeError at /jsi18n/
# https://github.com/edx/course-discovery/pull/2860
RUN curl https://github.com/edx/course-discovery/commit/cbbefd56a4efa67070288e94a260c5e069d035d6.patch | git apply -

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

# Install python and nodejs requirements
# This is identical to "make production-requirements" but it was split in multiple
# instructions to benefit from docker image caching
RUN pip install -r requirements.txt
ARG NPM_REGISTRY=https://registry.npmjs.org/
RUN npm install --verbose --registry=$NPM_REGISTRY --production
RUN ./node_modules/.bin/bower install --allow-root --production

# Install django-redis for using redis as a django cache
RUN pip install django-redis==4.12.1

# Install uwsgi
RUN pip install uwsgi==2.0.19.1

# Collect static assets
COPY assets.py ./course_discovery/settings/assets.py
ENV DJANGO_SETTINGS_MODULE course_discovery.settings.assets
RUN make static

EXPOSE 8000
CMD uwsgi \
    --static-map /static=/openedx/discovery/course_discovery/assets \
    --static-map /media=/openedx/discovery/course_discovery/media \
    --http 0.0.0.0:8000 \
    --thunder-lock \
    --single-interpreter \
    --enable-threads \
    --processes=2 \
    --wsgi-file course_discovery/wsgi.py
