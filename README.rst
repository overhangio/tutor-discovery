Course Discovery plugin for `Tutor <https://docs.tutor.overhang.io>`_
=====================================================================

This is a plugin for `Tutor <https://docs.tutor.overhang.io>`_ that integrates the `Course Discovery <https://github.com/edx/course-discovery/>`__ application in an Open edX platform. it is useful for integration with, for example, `Ecommerce <https://github.com/edx/ecommerce>`__ or an external course catalog.

.. image:: https://overhang.io/images/clients/e-ducation.jpg
    :alt: E-ducation
    :target: https://www.e-ducation.cn/

This plugin was developed and open sourced to the community thanks to the generous support of `E-ducation <https://www.e-ducation.cn/>`_. Thank you!

Installation
------------

This plugin requires tutor>=3.6.0. Also, you should have installed tutor from source, and not from a pre-compiled binary.

::
  
    pip install tutor-discovery

Then, to enable this plugin, run::
  
    tutor plugins enable discovery

You will have to re-generate the environment::
  
    tutor config save
    
The, run migrations migrations::
  
    tutor local init

This last step is unnecessary if you run instead ``tutor local quickstart``.

Operations
----------

Creating a user
~~~~~~~~~~~~~~~

The discovery user interface will be available at http://discovery.localhost for a local instance, and at ``DISCOVERY_HOST`` (by default: http(s)://discovery.<your lms host>) in production. In order to run commands from the UI, a user must be created::
  
  tutor local run discovery ./manage.py createsuperuser

Then, you must login with this user at http://discovery.localhost/admin.

Alternatively, you can login with oauth2 using a pre-existing user created on the LMS/CMS by accessing http(s)://discovery.<your lms host>/login. To do so, the proper domain names must exist and point to the production server.

Re-indexing courses
~~~~~~~~~~~~~~~~~~~

::
  
  tutor local run discovery ./manage.py refresh_course_metadata
  tutor local run discovery ./manage.py update_index --disable-change-limit
