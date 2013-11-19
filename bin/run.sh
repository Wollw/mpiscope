#!/usr/bin/env bash

if [[ $OSTYPE == darwin* ]]; then
    MPIRUN=openmpirun;
else
    MPIRUN=mpirun;
fi

$MPIRUN --hostfile etc/hostfile.local -np 3 python2 bin/example.py
