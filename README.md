# Heimdall

Secure gateway software for outgoing connections. This project will filter all
outgoing traffic and notify the user of unsecure protocol usage.

This project will be done using C and it will also make use of low level
interaction with the Linux operating system.


The secure gateway implemented for a Raspberry Pi, this will be a small example
of the capabilities of the Heimdall project. The main goal is to simply read a
configuration file witha all the restricted protocols.
All of the protocols are categorized by blocked, notify or both. Another
category would be secure, this is the opposite of the blocked, and all the
connections that use the secure label would be rerouted to the Internet. Also
all of the traffic inside the LAN range may or may not be resricted based on
new sets of rules.

The firectory organization is as follows:
	- database -- will be the database speficitation and initialization scrips
	- firewall -- holds the source code for the firewall system
	- companion -- is the companion app implementation of the entire system
	- web_service -- consists of the implementation of teh web service API
