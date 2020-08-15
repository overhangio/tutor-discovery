Course Discovery plugin for `Tutor <https://docs.tutor.overhang.io>`_
=====================================================================

This is a plugin for `Tutor <https://docs.tutor.overhang.io>`_ that integrates the `Course Discovery <https://github.com/edx/course-discovery/>`__ application in an Open edX platform. it is useful for integration with, for example, `Ecommerce <https://github.com/edx/ecommerce>`__ or an external course catalog.

.. image:: https://overhang.io/static/marketing/img/clients/e-ducation.jpg
    :alt: E-ducation
    :target: https://www.e-ducation.cn/

This plugin was developed and open sourced to the community thanks to the generous support of `E-ducation <https://www.e-ducation.cn/>`_. Thank you!

Installation
------------

This plugin requires tutor>=3.6.0. If you have installed tutor from a pre-compiled binary, it already comes bundled with the discovery plugin. Otherwise::

    pip install tutor-discovery

Then, to enable this plugin, run::

    tutor plugins enable discovery

You will have to re-generate the environment::

    tutor config save

The, run migrations::

    tutor local init

This last step is unnecessary if you run instead ``tutor local quickstart``.

Operations
----------

Creating a user
~~~~~~~~~~~~~~~

The discovery user interface will be available at http://discovery.local.overhang.io for a local test instance, and at ``DISCOVERY_HOST`` (by default: http(s)://discovery.<your lms host>) in production. In order to run commands from the UI, a user must be created::

  tutor local run discovery ./manage.py createsuperuser

Then, you must login with this user at http://discovery.local.overhang.io/admin.

Alternatively, you can login with oauth2 using a pre-existing user created on the LMS/CMS by accessing http(s)://discovery.<your lms host>/login. To do so, the proper domain names must exist and point to the production server.

Re-indexing courses
~~~~~~~~~~~~~~~~~~~

::

  tutor local run discovery ./manage.py refresh_course_metadata --partner_code=openedx
  tutor local run discovery ./manage.py update_index --disable-change-limit

Caching programs
~~~~~~~~~~~~~~~~

In order to cache programs in the LMS, you will need to manually create a catalog integration. This step should be performed just once::

    tutor local run lms ./manage.py lms create_catalog_integrations --enabled \
        --internal_api_url=http://discovery:8000/api/v1 \
        --service_username=lms_catalog_service_user

Then::

    tutor local run lms ./manage.py lms cache_programs

Debugging
---------

To debug the course discovery service, you are encouraged to mount the course-discovery repo from the host in the development container:

    tutor dev runserver -v ~/projets/openedx/repos/course-discovery/:/openedx/discovery discovery

You can then access the development server at http://discovery.local.overhang.io:8381. Feel free to add breakpoints (``import pdb; pdb.set_trace()``) anywhere in your source code to debug your application.

Alternatively, you may bind-mount a local course-discovery repository by adding the following to ``$(tutor config printroot)/env/dev/docker-compose.override.yml``::

    version: "3.7"
    services:
        discovery:
            volumes:
                - /path/to/course-discovery/:/openedx/discovery

Once a local repository is mounted in the image, you will have to install nodejs dependencies and collect static assets::

    tutor dev run discovery npm install --development
    tutor dev run discovery make static.dev

License
-------

This work is licensed under the terms of the `GNU Affero General Public License (AGPL) <https://github.com/overhangio/tutor/blob/master/LICENSE.txt>`_.
