ConfMan: Configuration Management via Python3 & CLI
======================================================

.. image:: https://img.shields.io/badge/ConfMan-Python3-blue

.. image:: https://img.shields.io/badge/EC--429-Website-brightgreen
    :target: https://errorcode429.com/

ConfMan is a python3 program designed to perform Secure Configuration Management functions.

Features
--------

- Perform baseline configurations
- Perform baseline configuration audits
- Perform baseline configuration change detections
- Perform baseline configuration promotions



Quick Start
-----------

To install ConfMan & python3 libraries, simply:

.. code-block:: bash

    $ git clone https://github.com/EC-429/ConfMan
    $ mkdir Managed
    $ pip install argparse
    $ pip install json
    $ pip install time
    $ import hashlib
    $ from colorama import Style, Back, Fore

Running the program:
.. code-block:: bash

    $ python3 ConfMan.py --help
    $ python3 ConfMan.py --baseline [/file/path] [baseline name] [appoved by]
    $ python3 ConfMan.py --audit [baseline name]
    $ python3 ConfMan.py --detect [baseline name]
    $ python3 ConfMan.py --promote [baseline name]


Documentation
-------------

Documentation is available at:
- `ConfMan youtube video <https://www.youtube.com/watch?v=3seJTAycQyM>`_
