Server Config
=============

Introduction
------------

This project contains two pieces- a simple web server using flask, and a tool to distribute that
application to a list of hosts and ensure compliance.

Web Server
----------

The application is very small, just the contents of ``server.py``, and uses pex_ to enforce a static
environment that isn't impacted by what else is running on the host. Under the ``debian`` directory
lie the files for packaging the ``deb`` which is installed on hosts.

Build - build.sh
----------------

There is a Vagrantfile_ in the top of the repository, which is configured to use Virtualbox_ by
default. This is what is used to build the ``deb`` package.

Deploy - deploy.sh
------------------

The ``Server Config`` tool itself uses a hostlist to perform its operations. Each list of hosts
places them into a 'role' determined by the file name. The tool, when called with a filename as its
argument, will check its commands for a matching set of configuration steps to perform, then
operate on each of the hosts in turn, ensuring compliance with the requisite pattern.


.. _pex: https://pex.readthedocs.org
.. _Vagrantfile: http://vagrantup.com
.. _Virtualbox: http://virtualbox.org