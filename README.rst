hub
==========================

.. image:: https://travis-ci.com/luizalabs/hub.svg
    :target: https://travis-ci.com/luizalabs/hub

Installation
------------

Create a virtualenv (use ``virtualenvwrapper``): ::

    mkvirtualenv hub


Install environment to development: ::

    make install-dev


`Setup the environment vars`_ or create a file ``django/hub/settings.ini`` with the content:


.. code:: ini

   [settings]
   DEBUG=true
   CHANGELOG_API_TOKEN=
   DEFAULT_FROM_EMAIL=your-email@example.com
   AWS_SES_ACCESS_KEY_ID=
   AWS_SES_SECRET_ACCESS_KEY=
   SECRET_KEY=SOME SECRET


.. _Setup the environment vars: http://barkas.com/2016/set-environment-variables-activating-virtualenv/

Run the project: ::

    make runserver


Tests
-----

To run the test suite, execute: ::

    make test


To show coverage details (in HTML), use: ::

    make test html
