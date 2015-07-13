.. default-role:: code

Wheelhouse
####################

Wheelhouse is a utility to help maintain a wheelhouse.

What is a Wheelhouse?
=====================

A wheelhouse is a local cache of python packages in wheel format that gets committed with your code
to your VCS. When installing packages during continuous integration and production, the wheels in
the wheelhouse are used instead of depending on PyPI or some other network location.

Advantages:
-----------

* Wheels are stored in your DVCS bringing further clarity to exactly what packages are
  needed/expected and how they have changed over time.
* CI builds are faster and more consistent.  Due to the increased speed of installing wheels from
  a local cache instead of pulling them from a network location, we can have tox start with a new
  virtualenv before every run, thereby insuring all dependencies have been specified and installed
  into the wheelhouse correctly.
* Production deployments are similarly fast and consistent.  Since the CI and production servers
  both pull from the same wheelhouse we have higher certainty that our production code is running
  against the exact same packages that have been tested.
* Since wheels are built on development or build machines, the need for development system packages
  to be installed on production servers is removed.
* Targeting forks, development versions, unpublished, and/or private software for production is
  much easier than setting up & maintaining a private PyPI server like `devpi`_.
* Splits the package management process into two distinct steps:

  #. Build packages (from various locations, with specified version) and put wheels in the
     wheelhouse.
  #. Install the latest version of a package from the wheelhouse.

.. _devpi: http://doc.devpi.net/latest/

Disadvantages:
--------------

* Some may be opposed to storing binary packages in version control.
* More disk space is needed for the binary packages.
* The wheelhouse will accumulate packages if not cleaned up regularly.  The `purge` command can
  help with this.

Example Usage
===============

Build/Refresh the Wheelhouse
----------------------------

This will build wheels and store them in the wheelhouse for any updated packages::

    wheelhouse build

Setting Up an Environment
-------------------------

Create a temporary virtualenv with packages installed from the wheelhouse::

    vex -mr myproj # or: mktmpenv
    wheelhouse install -- -r requirements/dev-env.txt
    pip install -e .

Your virtualenv now contains the same packages as the wheelhouse.  By using temporary environments
you force yourself to always work with what is in the wheelhouse.  Getting a package into your
development environment requires you to go throught the wheelhouse to do it. This means maintaining
the project's packages becomes a first-priority issue in every developers workflow.

Example Project
===============

The code for this project is rather basic, but it's the concept that counts. Putting the
concept of a wheelhouse into practice has made managing dependencies for our projects across dev,
testing and production environments much, much easier.

Checkout `Keg`_ to see a project which is using a wheelhouse in conjunction with tox to manage
dependencies.

.. _Keg: https://github.com/level12/keg


Current Features:
=================

* `build`: Will build all packages for all requirements file specified in the
  config file and store in the wheelhouse directory. Can also be passed the names of individual
  packages or aliases.
* `config`: display the configuration `wheelhouse` is using.
* `purge`: purge the wheelhouse of any wheel that isn't the most recent version in the wheelhouse
  for that package.

Possible Future Features:
=========================

* `install`: install a package/wheel from the wheelhouse.
* `status`: compare the working environment's installed packages with the requirement files, the
  wheelhouse, and package indexes (PyPI) and show where they are out of sync.


pip Configuration
=================

Once you have a wheelhouse (`wheelhouse build`), you can tell pip to install only from the
wheelhouse. To do that with environment variables and a tox.ini, it would look like::

    # tox.ini
    [testenv]
    setenv =
        PIP_USE_WHEEL=true
        PIP_NO_INDEX=true
        PIP_FIND_LINKS=requirements/wheelhouse

or, from the command line::

    pip install --use-wheel --no-index --find-links=requirements/wheelhouse -r requirements/testing.txt


Configuration
===============

You must place a `wheelhouse.ini` in the base of your project.  This is considered the "project
root" and all relative file paths are calculated from this location.

You may also place a `wheelhouse.ini` file in a user-specific location to override defaults for
Wheelhouse. See `wheelhouse config` for more information.

Config files are read by a `SafeConfigParser`_ instance.  See the linked docs for interpolation
support available.

.. _SafeConfigParser: https://docs.python.org/2/library/configparser.html#ConfigParser.SafeConfigParser

An example configuration file follows::

    [wheelhouse]
    # These files are relative to the project's requirements directory (default: `requirements/`).
    requirement_files =
        build.txt

    # Make sure each package has a wheel built for python 2 & 3.
    pip_bins = pip, pip3.4

    [aliases]
    # Shortcuts to be used when specifying projects to `build`.
    keg = https://github.com/level12/keg/zipball/master
    ke = https://github.com/level12/keg-elements/zipball/master


Issues & Discussion
====================

Please direct questions, comments, bugs, feature requests, etc. to:
https://github.com/level12/wheelhouse/issues

Current Status
==============

Very Beta, expect changes.

Development
===============

To develop on this project, begin by running our tests::

    git clone https://github.com/level12/wheelhouse wheelhouse-src
    cd wheelhouse-src
    tox

You can then examine tox.ini for insights into our development process.  In particular, we:

* use `py.test` for testing (and coverage analysis)
* use `flake8` for linting
* store `pip` requirements files in `requirements/`
* cache wheels in `requirements/wheelhouse` for faster & more reliable CI builds

Dependency Management
---------------------

Adding a dependency involves:

#. If it's a run-time dependency, add to `setup.py`.
#. Adding the dependency to one of the requirements files in `requirements/`.
#. Running `wheelhouse build`.

Preview Readme
--------------

When updating the readme, use `restview --long-description` to preview changes.

