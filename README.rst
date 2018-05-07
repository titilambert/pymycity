########
PyMyCity
########

Supported cities
################

* Mascouche: https://ville.mascouche.qc.ca
* Montréal: http://ville.montreal.qc.ca

Installation
############

::

    pip install pymycity


Usage
#####

::

    ± pymycity 
    usage: pymycity [-h] [-T TIMEOUT] {mascouche,montreal} ...


    Cities:
        * mascouche:
            + garbage_collection:
                - List next garbage collection
            + taxes:
                - List next taxes dates
            + events:
                - List next city events
        * montreal:
            + taxes:
                - List next taxes dates

Dev env
#######

::

    virtualenv -p /usr/bin/python3 env
    pip install -r requirements.txt
