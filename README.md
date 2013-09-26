metering-oml
============

Metering agents and applications using OML project.

# wiki of OML project
* http://mytestbed.net/projects/oml/wiki

# Installation Phase (server/collector side)
The reference Operating System is an Ubuntu-server 12.04 (ubuntu-12.04.2-server-amd64)
* user/password: oml/oml
* sudo apt-get update && sudo apt-get upgrade

Installing the common packages:
* adding sources list file: /etc/apt/sources.list.d/oml2.list
* adding repository: deb http://download.opensuse.org/repositories/home:cdwertmann:oml/xUbuntu_12.04/ /
* getting key: sudo wget http://download.opensuse.org/repositories/home:cdwertmann:oml/xUbuntu_12.04/Release.key
* adding key: sudo apt-key add - < Release.key
* sudo apt-get update
* sudo apt-get install liboml2 oml2-example

Installing the server packages:
* sudo apt-get install oml2-server
* (just in case you want to graphically examinate SQlite DB) sudo apt-get install sqlitebrowser

We have chosen (default) SQlite-DB as backend.
You can start|stop|restart oml2-server normally:
* sudo service <> start|stop|restart

Configuring the server at /etc/default/oml2-server:
* -l, --listen=3003                 Port to listen for TCP based clients
* -D, --data-dir=/opt/oml-db        Directory to store database files (sqlite)
* --user=oml                        Change server user id
* --group=oml                       Change server group id
* -d, --debug-level=4               Increase debug level (4=debug, ...)
* --logfile=/var/log/oml_server.log File to log to

Testing our (local) server test-bed:
* oml2-generator --amplitude 1 --frequency 1000 --samples 10 --sample-interval .1 \
        --oml-id localservertest --oml-domain installtest --oml-collect localhost
* sqlitebrowser /opt/oml-db/installtest.sq3

# Installation Phase (client/agents side)
* sudo apt-get install python-pip
* sudo pip install oml4py
