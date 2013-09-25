metering-oml
============

Metering agents and applications using OML project.

# wiki of OML project
* http://mytestbed.net/projects/oml/wiki

# Installation Phase
The reference Operating System is an Ubuntu-server 12.04 (ubuntu-12.04.2-server-amd64)
* user/password: oml/oml
* sudo apt-get update && sudo apt-get upgrade

Installing the common packages:
* adding sources list file: /etc/apt/sources.list.d/oml2.list
* adding repository: deb http://download.opensuse.org/repositories/home:cdwertmann:oml/xUbuntu_12.04/ /
* getting key:
** sudo wget http://download.opensuse.org/repositories/home:cdwertmann:oml/xUbuntu_12.04/Release.key
** sudo apt-key add - < Release.key
* sudo apt-get update
* sudo apt-get install liboml2 oml2-example

Installing the server packages:
* sudo apt-get install oml2-server
* (just in case you want to graphically examinate SQlite DB) sudo apt-get install sqlitebrowser

We have chosen (default) SQlite-DB as backend.
You can start|stop|restart oml2-server normally: sudo service <> start|stop|restart
