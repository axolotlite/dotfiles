#!/bin/bash

if [[ $(swaymsg -t get_outputs | grep name | wc -l) -ge 2 ]]; then
	echo success
        swaymsg input type:touch calibration_matrix -- -1 0 1 0 -0.5 1
        swaymsg input type:tablet_tool calibration_matrix -- -1 0 1 0 -0.5 1
else
	python -m rotate.py
fi
