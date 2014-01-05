#!/usr/bin/env bash

if [[ $OSTYPE == darwin* ]]; then
    PYTHON=python3;
    MPIRUN=openmpirun;
else
    PYTHON=python3;
    MPIRUN=mpirun;
fi

$MPIRUN --hostfile etc/hostfile.local -np 3 $PYTHON bin/example.py
