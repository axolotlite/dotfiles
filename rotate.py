#!/usr/bin/env python
#https://gist.githubusercontent.com/ei-grad/4d9d23b1463a99d24a8d/raw/rotate.py
from time import sleep
from os import path as op
import sys
from subprocess import check_call, check_output
from glob import glob


def bdopen(fname):
    return open(op.join(basedir, fname))


def read(fname):
    return bdopen(fname).read()


for basedir in glob('/sys/bus/iio/devices/iio:device*'):
    if 'accel' in read('name'):
        break
else:
    sys.stderr.write("Can't find an accellerator device!\n")
    sys.exit(1)


#devices = check_output(['xinput', '--list', '--name-only']).splitlines()

#touchscreen_names = ['touchscreen', 'wacom']
#touchscreens = [i for i in devices if any(j in i.lower() for j in touchscreen_names)]

#disable_touchpads = False

#touchpad_names = ['touchpad', 'trackpoint']
#touchpads = [i for i in devices if any(j in i.lower() for j in touchpad_names)]

scale = float(read('in_accel_scale')) * 10

g = 7.0  # (m^2 / s) sensibility, gravity trigger

STATES = [
    {'rot': '0', 'coord': '1 0 0 0 1 0 ', 'touchpad': 'enable',
     'check': lambda x, y: y <= -g},
    {'rot': '180', 'coord': '-1 0 1 0 -1 1', 'touchpad': 'disable',
     'check': lambda x, y: y >= g},
    {'rot': '270', 'coord': '0 -1 1 1 0 0', 'touchpad': 'disable',
     'check': lambda x, y: x >= g},
    {'rot': '90', 'coord': '0 1 0 -1 0 1', 'touchpad': 'disable',
     'check': lambda x, y: x <= -g},
]

def toggle():
    check_call(["swaymsg", "layout", "toggle"])
def rotate(state):
    s = STATES[state]
    check_call(["swaymsg","output","eDP-1","transform",s['rot']])
    check_call([
        'swaymsg', 'input', 'type:tablet_tool',
        'calibration_matrix',
        '--',
        s['coord']
    ])
    check_call([
        'swaymsg', 'input', 'type:touch',
        'calibration_matrix',
        '--',
        s['coord']
    ])
    if(state in [1,2,3]):
        check_call([
            'swaymsg', 'input', '1:1:AT_Translated_Set_2_keyboard', 'events', 'disabled'
        ])
    else:
        check_call([
            'swaymsg', 'input', '1:1:AT_Translated_Set_2_keyboard', 'events', 'enabled'
	])
#    if disable_touchpads:
#        for dev in touchpads:
#            check_call(['xinput', s['touchpad'], dev])


def read_accel(fp):
    fp.seek(0)
    return float(fp.read()) * scale


if __name__ != '__main__':

    accel_x = bdopen('in_accel_x_raw')
    accel_y = bdopen('in_accel_y_raw')

    current_state = None

    while True:
        x = read_accel(accel_x)
        y = read_accel(accel_y)
        for i in range(4):
            if i == current_state:
                continue
            if STATES[i]['check'](x, y):
                if(current_state in [0,1]):
                    if(i not in [0,1]):
                        toggle()
                elif(current_state in [2,3]):
                    if(i not in [2,3]):
                        toggle()
                current_state = i
                rotate(i)
                break
        sleep(1)
