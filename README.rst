
HCC API Document
================

HCC (Hyper Clustering Computing) API Document is in ``hcc/doc/``.
build it with::

    cd hcc/doc && make html

The doc will be at ``hcc/doc/_build/html/index.html``. Open it with your
favorite browser.


Contributor
===========

``hcc/`` is written by me.
``application.py`` is written by chihhsin.
``static/* templates/*`` is written by gxlkhhc and yongcing.


Sensitive Files
===============

======================================= ================================
hcc/ssh_setting/config                  key path, stack gateway ip.
hcc/ssh_setting/hhc.pem.template        VM private key.
hcc/ssh_setting/keypair.pem.template    stack gateway private key.
hcc/stack_api/senv.template             Openstack environment.
hcc/stack_api/credentials.py.template   Openstack environment.
hcc/stack_api/__init__.py               Absolute path, VM settings.
hcc/utils.py                            Absolute path.
application.py                          Server ip address.
static/js/hcc.js                        Server ip address.
======================================= ================================

And more Openstack-relative settings...

This project is done by me and my 3 teammates within 15 hr or less, from
brain stromming and defining APIs, to implements all and testing. Because
the deadline was tommorrow...XD

