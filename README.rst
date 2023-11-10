Course Discovery plugin for `Tutor <https://docs.tutor.edly.io>`_
=====================================================================

This is a plugin for `Tutor <https://docs.tutor.edly.io>`_ that integrates the `Course Discovery <https://github.com/edx/course-discovery/>`__ application in an Open edX platform. it is useful for integration with, for example, `Ecommerce <https://github.com/edx/ecommerce>`__ or an external course catalog.

Installation
------------

This plugin requires tutor>=3.6.0. If you have installed tutor from a pre-compiled binary, it already comes bundled with the discovery plugin. Otherwise::

    tutor plugins install discovery

Then, to enable this plugin, run::

    tutor plugins enable discovery

Restart and initialize your platform with::

    tutor local launch

Operations
----------

Creating a user
~~~~~~~~~~~~~~~

The discovery user interface will be available at http://discovery.local.edly.io for a local test instance, and at ``DISCOVERY_HOST`` (by default: http(s)://discovery.<your lms host>) in production. In order to run commands from the UI, a user must be created::

    tutor local run discovery ./manage.py createsuperuser

Then, you must login with this user at http://discovery.local.edly.io/admin.

Alternatively, you can login with oauth2 using a pre-existing user created on the LMS/CMS by accessing http(s)://discovery.<your lms host>/login. To do so, the proper domain names must exist and point to the production server.

Index configuration
~~~~~~~~~~~~~~~~~~~

Discovery uses separate indices for different models (the names are: course, course_run, person and program by default). And you can overwrite theses
names by configuring ``DISCOVERY_INDEX_OVERRIDES``::

    DISCOVERY_INDEX_OVERRIDES:
      course_discovery.apps.course_metadata.search_indexes.documents.course: your-course-index-name
      course_discovery.apps.course_metadata.search_indexes.documents.course_run: your-course-run-index-name
      course_discovery.apps.course_metadata.search_indexes.documents.person: your-person-index-name
      course_discovery.apps.course_metadata.search_indexes.documents.program: your-program-index-name

Re-indexing courses
~~~~~~~~~~~~~~~~~~~

::

    tutor local run discovery ./manage.py refresh_course_metadata --partner_code=openedx
    tutor local run discovery ./manage.py update_index --disable-change-limit

Caching programs
~~~~~~~~~~~~~~~~

In order to cache programs in the LMS, you will need to manually create a catalog integration. Make sure you use staff user for the below command. If ``lms_catalog_service_user`` is not a staff user, then make it a staff user in your LMS User model. This step should be performed just once::

    tutor local run lms ./manage.py lms create_catalog_integrations --enabled \
        --internal_api_url="" \
        --service_username=lms_catalog_service_user

Then run the below command, this command will cause errors every time as it tries to cache programs from all sites that are added to your LMS sites model::

    tutor local run lms ./manage.py lms cache_programs

If you don't want the errors, then make use of an extra argument to the command .i.e. ``--domain``. This argument will be equal to ``local.edly.io`` if you are running tutor local and ``local.edly.io:8000`` if you are running tutor dev::
    tutor local run lms ./manage.py lms cache_programs --domain="local.edly.io"
    or
    tutor dev run lms ./manage.py lms cache_programs --domain="local.edly.io:8000"

This last step should be performed every time you create new or make changes to existing programs.

Install extra requirements
~~~~~~~~~~~~~~~~~~~~~~~~~~

In order to install extra requirements, use DISCOVERY_EXTRA_PIP_REQUIREMENTS and re-build the docker image.::

  tutor config save \
    --set 'DISCOVERY_EXTRA_PIP_REQUIREMENTS=["git+https://github.com/myusername/myplugin"]'

Then, build the image, pointing to your fork if necessary::

  tutor images build discovery

Debugging
---------

To debug the course discovery service, you are encouraged to mount the course-discovery repo from the host in the development container:

    tutor dev start --mount /path/to/course-discovery/ discovery

You can then access the development server at http://discovery.local.edly.io:8381. Feel free to add breakpoints (``import pdb; pdb.set_trace()``) anywhere in your source code to debug your application.

Once a local repository is mounted in the image, you will have to install nodejs dependencies and collect static assets::

    tutor dev run discovery npm install --development
    tutor dev run discovery make static.dev

Troubleshooting
---------------

This Tutor plugin is maintained by Muhammad Faraz Maqsood from `Edly <https://edly.io/>`__. Community support is available from the official `Open edX forum <https://discuss.openedx.org>`__. Do you need help with this plugin? See the `troubleshooting <https://docs.tutor.edly.io/troubleshooting.html>`__ section from the Tutor documentation.


`Max retries exceeded with url`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When running in production with HTTPS enabled, you may face this error during the `init` phase of `tutor local launch`:

```
requests.exceptions.ConnectionError: HTTPSConnectionPool(host='<LMS_HOST>', port=443): Max retries exceeded with url: /api/courses/v1/courses/?page=1&page_size=10&username=discovery
```

This error may be due to an incorrect DNS resolution of the LMS DNS record. With some cloud providers (for instance: [DigitalOcean](https://digitalocean.com/)) the `/etc/hosts` file on the host automatically contains the following entry::

    127.0.1.1 <LMS HOST>

This entry may be present if you named your server with the LMS hostname.

License
-------

This work is licensed under the terms of the `GNU Affero General Public License (AGPL) <https://github.com/overhangio/tutor/blob/master/LICENSE.txt>`_.
