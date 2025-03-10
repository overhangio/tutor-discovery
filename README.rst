Course Discovery plugin for `Tutor`_
====================================

This is a plugin for `Tutor`_ that integrates the `Course Discovery`_ application in an Open edX platform.
it is useful for integration with, for example, `Ecommerce`_ or an external course catalog.


.. _Tutor: https://docs.tutor.edly.io
.. _Course Discovery: https://github.com/edx/course-discovery/
.. _Ecommerce: https://github.com/edx/ecommerce

Installation
------------

This plugin requires ``tutor>=3.6.0``. If you have installed tutor from a pre-compiled binary,
it already comes bundled with the discovery plugin. Otherwise:

.. code-block:: bash


    tutor plugins install discovery

Then, to enable this plugin, run:

.. code-block:: bash

    tutor plugins enable discovery

Restart and initialize your platform with:

.. code-block:: bash

    tutor dev|local|k8s launch

Operations
----------

Creating a user
~~~~~~~~~~~~~~~

The discovery user interface will be available at http://discovery.local.openedx.io for a local test instance,
and at ``DISCOVERY_HOST`` (by default: http(s)://discovery.<your lms host>) in production. To run
commands from the UI, a user must be created:

.. code-block:: bash

    tutor local run discovery ./manage.py createsuperuser

Then, you must log in with this user at http://discovery.local.openedx.io/admin.

Using SSO with LMS
~~~~~~~~~~~~~~~~~~

If you want to log in using Single Sign-On (SSO) with the LMS, ensure that the superuser you created 
above in discovery has the same username and email as an existing admin user in the LMS/CMS. You can 
then access the discovery interface via `http(s)://discovery.<your lms host>/login`. Make sure that 
the proper domain names are configured and point to the production server.

Index configuration
~~~~~~~~~~~~~~~~~~~

Discovery uses separate indices for different models (the names are: course, course_run, person, and
program by default). And you can overwrite these names by configuring ``DISCOVERY_INDEX_OVERRIDES``:

.. code-block:: yml

    DISCOVERY_INDEX_OVERRIDES:
      course_discovery.apps.course_metadata.search_indexes.documents.course: your-course-index-name
      course_discovery.apps.course_metadata.search_indexes.documents.course_run: your-course-run-index-name
      course_discovery.apps.course_metadata.search_indexes.documents.person: your-person-index-name
      course_discovery.apps.course_metadata.search_indexes.documents.program: your-program-index-name

Re-indexing courses
~~~~~~~~~~~~~~~~~~~

While running tutor in production mode:

.. code-block:: bash

    tutor local run discovery ./manage.py refresh_course_metadata --partner_code=openedx
    tutor local run discovery ./manage.py update_index --disable-change-limit

While running tutor in development mode:

.. code-block:: bash

    tutor dev run discovery ./manage.py refresh_course_metadata --partner_code=dev
    tutor dev run discovery ./manage.py update_index --disable-change-limit

Caching programs
~~~~~~~~~~~~~~~~

To cache programs in the LMS, you will need to manually create a catalog integration.
Make sure you use staff user for the below command. If ``lms_catalog_service_user`` is not a staff user,
then make it a staff user in your LMS User model. This step should be performed just once:

.. code-block:: bash

    tutor local run lms ./manage.py lms create_catalog_integrations --enabled \
        --internal_api_url="" \
        --service_username=lms_catalog_service_user

Then run the below command, this command will cause errors every time it tries to cache programs
from all sites that are added to your LMS sites model:

.. code-block:: bash

    tutor local run lms ./manage.py lms cache_programs

The above command will give some errors as it tries to cache programs for all sites. So make use of an
extra argument to the command. i.e. ``--domain``. While running tutor in production mode:

.. code-block:: bash

    tutor local run lms ./manage.py lms cache_programs --domain="local.openedx.io"

While running tutor in development mode:

.. code-block:: bash

    tutor dev run lms ./manage.py lms cache_programs --domain="local.openedx.io:8000"

This last step should be performed every time you create new or make changes to existing programs.

Show Programs Tab
~~~~~~~~~~~~~~~~~

By default, the **Programs** tab is available in the LMS dashboard. Users can enable or disable this tab as needed.
To Disable Programs, run the following command:

.. code-block:: bash

    tutor config save --set ENABLE_PROGRAMS=False

To Enable Programs, run the following command:

.. code-block:: bash

    tutor config save --set ENABLE_PROGRAMS=True

Only programs in which learners are registered will appear on this page. If a learner is enrolled in any course that is part of a program, that program will be displayed here.

.. image:: https://github.com/overhangio/tutor-discovery/assets/122095701/e0224011-adc0-41e4-a104-af4cb0c24b82
    :alt: Programs Tab on LMS dashboard

In the image above, the **Explore Programs** button points to http://localhost:8080/programs by default. This link does not exist, so users can change it to their custom-built marketing site URL to display all programs.
To Modify the Link:

1. Go to the **Site Configurations** model in the LMS Admin Panel: `http://local.openedx.io/admin/site_configuration/siteconfiguration/`
2. Open the respective LMS site configuration.
3. Add the following dictionary in the **site values** field like in the below image:

.. code-block:: python

    "MKTG_URLS": {
        "ROOT": "https://custom-marketing-site-here.com"
    }

.. image:: https://github.com/overhangio/tutor-discovery/assets/122095701/2d588ea9-a830-40b6-9845-8fab56d7cb5a
    :alt: Add Custom Site for Explore Programs

By following above instructions, this link (https://custom-marketing-site-here.com) will be replaced by http://localhost:8080. Additionally, users can also replace "/programs" by following these below steps:

1. Go to: `http://local.openedx.io/admin/programs/programsapiconfig/`
2. Add **Marketing path** equal to "/programs" or your desired marketing site path and enable it.

Install extra requirements
~~~~~~~~~~~~~~~~~~~~~~~~~~

To install extra requirements, use ``DISCOVERY_EXTRA_PIP_REQUIREMENTS`` and re-build the docker image.

.. code-block:: bash

  tutor config save --set 'DISCOVERY_EXTRA_PIP_REQUIREMENTS=["git+https://github.com/myusername/myplugin"]'

Then, build the image, pointing to your fork if necessary:

.. code-block:: bash

  tutor images build discovery

Debugging
---------

To debug the course discovery service, you are encouraged to mount the course-discovery repo from the host
in the development container:

.. code-block:: bash

    tutor dev start --mount /path/to/course-discovery/ discovery

You can then access the development server at http://discovery.local.openedx.io:8381. Feel free to add breakpoints
(``import pdb; pdb.set_trace()``) anywhere in your source code to debug your application.

Once a local repository is mounted in the image, you will have to install nodejs dependencies and collect static assets:

.. code-block:: bash

    tutor dev run discovery npm install --development
    tutor dev run discovery make static.dev


`Max retries exceeded with url`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When running in production with HTTPS enabled, you may face this error during the `init` phase of `tutor local launch`:

.. code-block:: log

    requests.exceptions.ConnectionError: HTTPSConnectionPool(host='<LMS_HOST>', port=443): Max retries exceeded with url: /api/courses/v1/courses/?page=1&page_size=10&username=discovery

This error may be due to an incorrect DNS resolution of the LMS DNS record. With some cloud providers
(for instance: `DigitalOcean`_) the `/etc/hosts` file on the host automatically
contains the following entry:

.. code-block:: bash

    127.0.1.1 <LMS HOST>

This entry may be present if you named your server with the LMS hostname.

.. _DigitalOcean: https://digitalocean.com/


Using event-bus with tutor-discovery
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Although tutor-discovery does not start event bus consumption by default, it supports running it. To consume events from event bus with tutor-discovery, follow these `instructions`_ provided by `event-bus-redis`_.

.. _instructions: https://github.com/openedx/event-bus-redis/blob/main/docs/tutor_installation.rst
.. _event-bus-redis: https://github.com/openedx/event-bus-redis


Troubleshooting
---------------

This Tutor plugin is maintained by Muhammad Labeeb from `Edly`_.
Community support is available from the official `Open edX forum`_.
Do you need help with this plugin? See the `troubleshooting`_
section from the Tutor documentation.

.. _Edly: https://edly.io/
.. _Open edX forum: https://discuss.openedx.org
.. _troubleshooting: https://docs.tutor.edly.io/troubleshooting.html

License
-------

This work is licensed under the terms of the `GNU Affero General Public License (AGPL)`_.

.. _GNU Affero General Public License (AGPL): https://github.com/overhangio/tutor/blob/release/LICENSE.txt
