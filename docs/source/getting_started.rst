.. _getting_started:

Getting Started with Wiring-x86
===============================

Here are some easy instructions to get you up and running with the
``wiring-x86.py`` module.


Prerequisites
--------------

The ``wiring-x86.py`` module is meant to be used on Intel® Galileo Gen2
platform with its original YOCTO Linux OS. For more information on the Intel®
Galileo Gen2 board and how to get this software go to `Intel® Makers site
<https://communities.intel.com/community/makers>`_. This module will only work
with that combination of board and OS since it uses the Intel® Galileo Gen2
GPIO driver sysfs interface.

The ``wiring-x86.py`` module also requires Python 2.7 which is installed as standard on


Installing Wiring-x86
---------------------

The first step is to install the Wiring-x86 module. There are several ways to
do this.

Using PIP
*********

If available, the `pip <http://www.pip-installer.org/en/latest/index.html>`_
installer is the preferred method for installing Python modules from `PyPI
<http://pypi.python.org/pypi>`_, the Python Package Index::

    $ sudo pip install wiring-x86

Using Easy_Install
******************

If ``pip`` isn't available on your system then `easy_install
<http://peak.telecommunity.com/DevCenter/EasyInstall>`_ may be::

    $ sudo easy_install wiring-x86

Installing from a tarball
*************************

If you download a tarball of the latest version of wiring-x86 you can install
it as follows (change the version number to suit)::

    $ tar -zxvf wiring-x86-1.2.3.tar.gz

    $ cd wiring-x86-1.2.3
    $ sudo python setup.py install

A tarball of the latest code can be downloaded from GitHub as follows::

    $ curl -O -L http://github.com/emutex/wiring-x86/archive/master.tar.gz

    $ tar zxvf master.tar.gz
    $ cd wiring-x86-master/
    $ sudo python setup.py install


Cloning from GitHub
*******************

The Wiring-x86 source code and bug tracker is in the
`wiring-x86 repository <http://github.com/emutex/wiring-x86>`_ on GitHub.

You can clone the repository and install from it as follows::

    $ git clone https://github.com/emutex/wiring-x86.git

    $ cd wiring-x86
    $ sudo python setup.py install


Running a sample program
------------------------

The ``wiring-x86`` repository and tarball includes several example
programs. There are also shown in the :ref:`ex` section.
