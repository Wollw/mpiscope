#!/usr/bin/env bash

if [[ $OSTYPE == darwin* ]]; then
    PYTHON=python
    MPIRUN=openmpirun;
else
    PYTHON=python2
    MPIRUN=mpirun;
fi

$MPIRUN --hostfile etc/hostfile.local -np 3 $PYTHON bin/example.py
