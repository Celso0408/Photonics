#!/bin/bash

for d in `seq 0.02 0.02 0.30`; do
    python coupler.py -d ${d} |tee -a directional_coupler.out;
done
