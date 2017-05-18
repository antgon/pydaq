Getting started
===============

Requirements
------------

* Python 3.5 or above
* PyQt5
* [pyqtgraph](http://pyqtgraph.org) 0.10.0 or above
* [python serial](https://github.com/pyserial/pyserial) 3.0 or above
* [edfrw](https://github.com/antgon/edfrw)

On Debian and friends, running as su the following should do the job:

`apt-get install python3-pyqtgraph python3-pyqt5 python3-serial`


Set-up the microcontroller
--------------------------

Pydaq works by sending a 'start' signal to the MCU and then repeatedly
reading data from the serial port from a pre-determined number of
channels (or signals). Thus, before starting, the microcontroller (MCU)
that will be reading and sending the data must be configured. The sample
file provided by pydaq in the firmware folder sets an mbed ready for
this, reading data from 3 ADC channels and sending them to pydaq.
Details about the firmware can be found below.


Launch pydaq
------------

After uploading the firmware to the MCU, pydaq can be launched by simply
running pydaq.py (e.g. `python3 pydaq.py`).
