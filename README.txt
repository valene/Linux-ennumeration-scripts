#BASIC LINUX ENNUMERATION SCRIPTS

Linux_Ennum.sh is a basic linux enumeration script 

customreconscan.py is a quick and dirty hack script should be usable for most situations but customise according to need.

sample_buffer_overflow_template.py is a simple template used to abstracting the process of buffer overflow 
by using commandline flags to control a single script for various stages of BO. Even thought it is meant as an abstraction,
the are points to be noted:

Hardcoded:
----------

* retadd

* badchars

* shellcode

Additional
-----------

* the strings to be send to the remote server, should be changed as per findings.

TODO
----

* -s flag is not need for certain stages but still used for checking, this should be changed.

* include retadd through commandline flags, probably through a regexp matching.

* call msfvenom from script for shell code, pros: less hardcoding, cons: maybe more commandline flags due to msfvenom encoders. 

* let it generate a final exploit code which can be just run and submitted to wherever needed. ? 
