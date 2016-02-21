Server Config
=============

Introduction
------------

This project contains a web application named ``hello_world`` and a tool to distribute that
application to a list of hosts and ensure compliance.

Web Source
----------

The application is contained within the ``hello_world`` directory, and the contents are zipped and
deployed onto each host. This application is deployed on ``webserver`` hosts, and relies on both
Apache and mod_php to be installed on its hosts.

Deploy - Server Config
----------------------

The ``Server Config`` tool itself uses a hostlist to perform its operations. Each list of hosts
places them into a 'role' determined by the file name. The tool, when called with a filename as its
argument, will check its commands for a matching set of configuration steps to perform, then
operate on each of the hosts in turn, ensuring compliance with the requisite pattern.

The tool is built with ``build.sh`` and can be run with an invocation along the lines of

``./server_config.pex --role=webserver --action=deploy``

There will need to be three files for that to work

- ``webserver.txt``: A list of hosts in the webserver role
- ``username``: The username to connect to each host as
- ``password``: The password to use to authenticate to each host

The entry point for the tool is ``command_line.py``, which uses a ``Dispatcher`` to identify how to
proceed. There are two main pieces which drive the configuration tool, Operators and Executors.

Operator
~~~~~~~~

Operators maintain the vast majority of overall coordination and business-logic. This is the place
to handle concurrency, determine how many hosts can be down at once, and also deal with rollbacks
if necessary.

Executor
~~~~~~~~

Each Executor is responsible for managing an individual host one step at a time. Typically since
these only focus on a single host, Operators can spin up multiple Executors to remotely connect
to other hosts and perform various operations. Typical examples involve installing packages,
modifying configuration values, and deploying new application code.
