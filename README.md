orientdb3-rpm
---------
A set of scripts to package orientb into an rpm. Skeleton borrowed from kafka-rpm which does the same thing.

Setup
-----
    $ yum groupinstall "Development Tools"

Building
--------
    $ make rpm ORIENTDB_VERSION=3.0.18

Resulting RPM will be avaliable at $(shell pwd)

Installing and operating
------------------------
    $ sudo yum install orientdb*.rpm
    $ sudo service orientdb start
    $ sudo orientdb kafka on

Libs, binaries, configs and logs are in /opt/orientdb.
Default config assumes zookeeper is installed at localhost.
