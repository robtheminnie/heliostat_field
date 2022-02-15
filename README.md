# Heliostat field

System consists of two main components, the master camera, 1 off, and the heliostats, multiple.  these are connected by 4 wires, uart rx, tx, +5v, GND, in a daisy chain configuration.
The master camera is node 0 of the chain, node 1 is the pi pico that drives the master camera  pan tilt platform.  Each node after that is a heliostat.

## Master camera
This handles the positioning of all heliostats.

## Heliostats
these are single heliostats, the position of which is controlled by the master camera.
