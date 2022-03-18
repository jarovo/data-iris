#!/bin/sh

OVERLAYS="bb030f id0074-slot12 ic006a-slot22 ic0073-slot32"

# create bootcmd.d artefact
echo "setenv overlay ${OVERLAYS}" >/etc/bootcmd.d/src/12-overlays.unused
