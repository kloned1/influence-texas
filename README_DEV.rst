influencetx
===========

`influencetx`: An `ATX Hack for Change`_ project for accessing Texas campaign finance and voting
records.

.. image:: https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg
     :target: https://github.com/pydanny/cookiecutter-django/
     :alt: Built with Cookiecutter Django


.. _ATX Hack for Change: http://atxhackforchange.org/


Setup
-----

- `Install Docker CE`_
- Clone code::
      cd your/code/directory
      git clone https://github.com/open-austin/influence-texas.git
- Start up docker container::
      cd influence-texas
      docker-compose up -d

The first time it's run `docker-compose` will pull down a generic python and postgres images
images. After that, it will install dependendencies specific to the app and start up a server for
the `influencetx` app at http://localhost:8000/.

.. _Install Docker CE: https://docs.docker.com/engine/installation/


Basic Commands
--------------

All of the basic commands are based off of the following commands for interacting with the docker
container:

- `docker-compose`_: Run generic docker commands in docker containers.
    - Run `docker-compose -h` to see a full list of commands.
    - Run `docker-compose help <COMMAND>` to see help on a command.
- `./pyinvoke.sh`: A shortcut for running invoke_ commands in docker containers.
    - Run `./pyinvoke.sh -l` to see a full list of commands.
    - Run `./pyinvoke.sh -h <COMMAND>` to see help on a command.
- `./djadmin.sh`: A shortcut for running `django admin`_ commands in docker containers.
    - Run `./djadmin.sh help` to see a full list of commands.
    - Run `./djadmin.sh help <COMMAND>` to see help on a command.

These instructions assume you're executing the command from the parent directory of this file. You
can find details of any commands using the commands above. A few commonly used commands are

.. _docker-compose: https://docs.docker.com/compose/reference/
.. _invoke: http://www.pyinvoke.org/
.. _django admin: https://docs.djangoproject.com/en/1.11/ref/django-admin/


Maintenance commands
....................

The commands commonly used for maintenance of this project are described below.

- `docker-compose up -d`: Start up docker container in detached mode (background task). You can
  keep a docker container running continuously, so you may only need to run this after restarting
  your machine.
- `./djadmin.sh makemigrations`: Make schema migrations to reflect your changes to Django models.
  Any migrations that you make should be committed and pushed with your model changes.
- `./djadmin.sh migrate`: Migrate database to the current schema. You'll need to run this after
  running `./djadmin.sh makemigrations` to actually apply migrations. If you pull code from github
  that includes migrations, you should run this to sync your database.
- `./pyinvoke.sh test`: Execute tests using pytest. At minimum, run this before committing code.
- `./pyinvoke.sh create-app`: Create `Django app`_. Django apps are small collections of
  functionality for your web application.

.. _Django app: https://docs.djangoproject.com/en/1.11/ref/applications/#projects-and-applications


Additional Docker commands
..........................

- `docker-compose up`: Start up docker container.
- `docker-compose down`: Shutdown docker container.
- `docker-compose logs`: Display bash output for all containers.
- `docker-compose logs web`: Display bash output for web container.
- `docker-compose logs ps`: Display list of containers.


Additional Django admin commands
................................

- `./djadmin.sh createsuperuser`: Create superuser account.


Live reloading and Sass CSS compilation
.......................................

Moved to `Live reloading and SASS compilation`_.

.. _`Live reloading and SASS compilation`: http://cookiecutter-django.readthedocs.io/en/latest/live-reloading-and-sass-compilation.html


Sentry
......

Sentry is an error logging aggregator service. You can sign up for a free account at
https://sentry.io/signup/?code=cookiecutter  or download and host it yourself.  The system is setup
with reasonable defaults, including 404 logging and integration with the WSGI application.

You must set the DSN url in production.


Settings
--------

Moved to settings_.

.. _settings: http://cookiecutter-django.readthedocs.io/en/latest/settings.html