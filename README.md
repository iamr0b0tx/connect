# connect
Adhoc that makes devices on the network into routers which creates a mini-internet setup. I tried to write relay script 
to access a device on a network that shares a client with the same device

## Setup
Using Socket programming in python a device running this program acts as a router pushing traffic (packets) through it to a said address on the network. It simulates the behaviour of a router when multiple networks are setup by different devices connected to to at leat one of this networks (__note__: a minimum of one device must connect two different networks together)

The setup was refactored to a Flask application to better handle the packets and avoid data curruption and easy handling of addresses (routing and API) and I/O operations.
