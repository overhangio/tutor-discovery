FROM ubuntu:16.04

RUN apt update && \
  apt install -y git-core language-pack-en python3 python3-pip python3-venv \
  build-essential libffi-dev libmysqlclient-dev libxml2-dev libxslt-dev libjpeg-dev libssl-dev
ENV LC_ALL en_US.UTF-8

RUN mkdir -p /openedx/discovery && \
    git clone https://github.com/edx/course-discovery.git --branch open-release/ironwood.2 --depth 1 /openedx/discovery
WORKDIR /openedx/discovery

# Setup minimal yml config file, which is required by production settings
COPY config.yml /openedx/config.yml
ENV DISCOVERY_CFG /openedx/config.yml

# Install python venv
RUN python3 -m venv ../venv/
ENV PATH "/openedx/venv/bin:$PATH"
RUN pip install --upgrade pip setuptools

# Install a recent version of nodejs
RUN pip install nodeenv
RUN nodeenv /openedx/nodeenv --node=8.9.3 --prebuilt
ENV PATH /openedx/nodeenv/bin:${PATH}

# Install python and nodejs requirements
# This is identical to "make production-requirements" but it was split in multiple
# instructions to benefit from docker image caching
RUN pip install -r requirements.txt
RUN npm install --production
RUN ./node_modules/.bin/bower install --allow-root --production

# Collect static assets
COPY assets.py ./course_discovery/settings/assets.py
ENV DJANGO_SETTINGS_MODULE course_discovery.settings.assets
RUN make static

EXPOSE 8000
CMD gunicorn --bind=0.0.0.0:8000 --workers 2 --max-requests=1000 course_discovery.wsgi:application
