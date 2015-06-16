.. default-role:: code

Wheelhouse
####################

Wheelhouse is a utility to help maintain a wheelhouse.

What is a Wheelhouse?
=====================

A wheelhouse is a project-specific directory where built eggs are stored.  When installing packages
during continuious integration and production, the eggs in the wheelhouse are used instead of
depending on PyPI or some other network location.

Advantages:
-----------

* Wheels are stored in your DVCS bringing further clarity to exactly what packages are
  needed/expected and how they have changed over time.
* CI builds are faster and more consistent.  Due to the increased speed of installing wheels from
  a local cache instead of pulling them from a network location, we can have tox start with a new
  virtualenv before every run, thereby insuring all depdencies have been specified and installed
  into the wheelhouse correctly.
* Production deployments are similiarily fast and consistent.  Since the CI and production servers
  both pull from the same wheelhouse we have higher certainty that our production code is running
  against the exact same pacakges that have been tested.
* Since wheels are built on development or build machines, the need for development system packages
  to be installed on production servers is removed.
* Targeting forks, development versions, unpublished, and/or private software for production is
  much easier than setting up & maintaining a private PyPI server like `devpi`.
* Splits the package management paradigm up into two distinct steps:

  #. Build packages (from various locations, with specified version) and put it in the wheelhouse
  #. Install the latest version of a package from the wheelhouse.

Disadvantages:
--------------

* Some may be opposed to storing binary packages in version control.
* More disk space is needed for the binary packages.
* The wheelhouse will accumlate packages if not cleaned up regularily.

Current Features:
=================

* `build`: Will build all packages for all requirements file specified in the
  config file and store in the wheelhouse directory. Can also be passed the names of individual
  packages or aliases.
* `config`: display the configuation`wheelhouse` is using.

Possible Future Features:
=========================

* `prune`: prunee the wheelhouse of old packages.
* `status`: compare the working environment's installed packages with the requirement files, the
  wheelhouse, and package indexes (PyPI) and show where they are out of sync.


Configuration
===============

You must place a `wheelhouse.ini` in the base of your project.  This is considered the "project
root" and all relative file paths are calculated from this location.

You may also place a `wheelhouse.ini` file in a user-specific location to override defaults for
Wheelhouse. See `wheelhouse config` for more information.

Config files are read by a `SafeConfigParser` instance.  See the linked docs for interpolation
support available.

.. SafeConfigParser: https://docs.python.org/2/library/configparser.html#ConfigParser.SafeConfigParser

An example configuration file follows.  Defaults for a Linux box are shown::

    # Wheelhouse will absolutize and normalize these paths.  Relative paths use the project root
    # as the base directory.
    requirements_path = requirements
    wheelhouse_path = requirements/wheelhouse

    requirements_files =
        runtime.txt
        testing.txt

    [aliases]
    keg = https://github.com/level12/keg/zipball/master
    ke = https://github.com/level12/keg-elements/zipball/master

Issues & Discussion
====================

Please direct questions, comments, bugs, feature requests, etc. to:
https://github.com/level12/wheelhouse/issues

Current Status
==============

Very Beta, expect changes.

