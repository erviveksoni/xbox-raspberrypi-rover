#!/usr/bin/python3

from __future__ import division

import Adafruit_PCA9685

pwm = Adafruit_PCA9685.PCA9685()
pwm.set_pwm_freq(60)
MIN_PULSE_WIDTH = 650
MAX_PULSE_WIDTH = 2350
FREQUENCY = 60
turn_error = 10

def turn_to_angle(angle):  
    angle = turn_error + angle
    pwm.set_pwm(2, 0, pulseWidth(angle))

def turn_middle():
    angle = turn_error + 90
    turn_to_angle(angle)

def map(x, in_min, in_max, out_min, out_max):
    return int((x-in_min) * (out_max-out_min) / (in_max-in_min) + out_min)

def pulseWidth(angle):
  pulse_wide   = map(angle, 0, 180, MIN_PULSE_WIDTH, MAX_PULSE_WIDTH)
  analog_value = int(float(pulse_wide) / 1000000 * FREQUENCY * 4096)
  return analog_value
