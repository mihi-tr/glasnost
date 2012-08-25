Glasnost
========

Introduction
------------

Glasnost is a measurement lab test that allows users to measure their
connection speed and whether their internet provider throttels certain
things. see http://measurementlab.net/measurement-lab-tools

The data collected by glasnost if freely available:
http://measurementlab.net/data

Requirements
------------

M-lab data

create a virtualenv::

    virtualenv env
    source env/bin/activate 

Now install the requirements::

    pip install -r requirements.txt

Download the geoip database from http://www.maxmind.com/download/geoip/database/GeoLiteCountry/
and edit your settings.py accordingly

go ahead and play with glasnost.py
