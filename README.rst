Server Config
=============

Introduction
------------

This project contains two pieces- a simple web server using flask, and a tool to distribute that
application to a list of hosts and ensure compliance.

Web Source
----------

The application is contained within the ``hello_world`` directory, and the contents are zipped and deployed onto each host.

Deploy - Server Config
----------------------

The ``Server Config`` tool itself uses a hostlist to perform its operations. Each list of hosts
places them into a 'role' determined by the file name. The tool, when called with a filename as its
argument, will check its commands for a matching set of configuration steps to perform, then
operate on each of the hosts in turn, ensuring compliance with the requisite pattern.

Hello World Configuration
-------------------------

The Hello World application currently depends on the Apache Web Server as well as mod_php to run its application code. The configuration for Apache lies within the hello_world module.
