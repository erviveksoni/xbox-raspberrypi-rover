#!/usr/bin/env python3

import asyncio
import math
import os
import signal
import sys
import threading
import time

import RPi.GPIO as GPIO
from evdev import InputDevice, ecodes, ff, list_devices
from rpi_ws281x import *

import gamepad
import led
import led_strip
import motor
import turn
from soundplayer import SoundPlayer

status     = 1          #Motor rotation
forward    = 1          #Motor forward
backward   = 0          #Motor backward

left_spd   = 100         #Speed of the car
right_spd  = 100         #Speed of the car

head_light_flag = False

def setup():
    motor.setup()
    led.setup()
    turn.turn_middle()
    led.green()

def turn_head(angle):
    turn.turn_to_angle(angle)

def turn_left_led():         #Turn on the LED on the left
    led.turn_left(4)

def turn_right_led():        #Turn on the LED on the right
    led.turn_right(4)

def drive_motor(direction, speed):    
    if direction == "forward":
        motor.motor_left(status, forward,left_spd*abs(speed))
        motor.motor_right(status,backward,right_spd*abs(speed))
    elif direction == "backward":
        motor.motor_left(status, backward, left_spd*abs(speed))
        motor.motor_right(status, forward, right_spd*abs(speed))
        if reverse_sound.isPlaying() == False:
            reverse_sound.play()
    else:
        motor.motorStop()
        if reverse_sound.isPlaying() == True:
            reverse_sound.play()

def get_motor_direction(x,y):
    if x == 0 and y == 0:
        return "stop"
    elif y >= 0:
        return "forward"
    
    return "backward"

def get_angle_from_coords(x,y):
    angle = 0.0
    if x==0.0 and y==0.0:
        angle = 90.0
    elif x>=0.0 and y>=0.0:
        # first quadrant
        angle = math.degrees(math.atan(y/x)) if x!=0.0 else 90.0
    elif x<0.0 and y>=0.0:
        # second quadrant
        angle = math.degrees(math.atan(y/x))
        angle += 180.0
    elif x<0.0 and y<0.0:
        # third quadrant
        angle = math.degrees(math.atan(y/x))
        angle += 180.0
    elif x>=0.0 and y<0.0:
        # third quadrant
        angle = math.degrees(math.atan(y/x)) if x!=0.0 else -90.0
        angle += 360.0
    return angle

def connect(): # asyncronus read-out of events
        xbox_path = None
        remote_control = None
        devices = [InputDevice(path) for path in list_devices()]
        print('Connecting to xbox controller...')
        for device in devices:
            if str.lower(device.name) == 'xbox wireless controller':
                xbox_path = str(device.path)
                remote_control = gamepad.gamepad(file = xbox_path)
                remote_control.rumble_effect = 2
                return remote_control
        return None

def is_connected(): # asyncronus read-out of events
    path = None
    devices = [InputDevice(path) for path in list_devices()]
    for device in devices:
        if str.lower(device.name) == 'xbox wireless controller':
            path = str(device.path)
    if(path == None):
        print('Xbox controller disconnected!!')
        return False
    return True

def led_thread():         #WS_2812 leds
    global head_light_flag

    while 1:
        if remote_control.dpad_up:
            siren_sound.play(1.0)
            led.police(4)
            time.sleep(0.1)
            siren_sound.stop()
        elif remote_control.dpad_right:
            led_strip.rainbowCycle(strip)
            time.sleep(0.1)
        elif remote_control.dpad_left:
            led_strip.theaterChaseRainbow(strip,50)
            time.sleep(0.1)
        elif remote_control.button_a:
            if head_light_flag:
                led.both_off()
                led_strip.colorWipe(strip, Color(0,0,0))
                head_light_flag = False
            elif head_light_flag == False:
                led.both_on()
                led_strip.colorWipe(strip, Color(255,0,0))
                head_light_flag = True
        else:
            pass
        time.sleep(0.1)

async def read_gamepad_inputs():
    global head_light_flag
    print("Ready to drive!!")
    turn_sound = SoundPlayer("/home/pi/xbox-raspberrypi-rover/soundfiles/turn-signal.mp3", 2)
    horn_sound = SoundPlayer("/home/pi/xbox-raspberrypi-rover/soundfiles/Horn.mp3", 2)        

    while is_connected() and remote_control.button_b == False:
        #print(" trigger_right = ", round(remote_control.trigger_right,2),end="\r")
        x = round(remote_control.joystick_left_x,2)
        y = round(remote_control.joystick_left_y,2)
        angle = get_angle_from_coords(x,y)
        if angle > 180:
            angle = 360 - angle
        #print("x:", x, " y:", y, " angle: ",angle,end="\r")
        turn_head(angle)
        direction = get_motor_direction(x,y)
        #print("x:", x, " y:", y, " direction: ",direction,end="\r")
        drive_motor(direction,y)

        if round(remote_control.trigger_right,2) > 0.0:
            horn_sound.play(1.0)
            led.blue()
        elif round(remote_control.trigger_left,2) > 0.0:
            led.cyan()
        elif remote_control.bump_left:
            turn_sound.play(1.0)
            led.turn_left(5)
        elif remote_control.bump_right:
            turn_sound.play(1.0)
            led.turn_right(5)
        elif remote_control.dpad_up:
            remote_control.dpad_up = False
        elif remote_control.dpad_left:
            remote_control.dpad_left = False
        elif remote_control.dpad_right:
            remote_control.dpad_right = False
        elif remote_control.button_a:
            remote_control.button_a = False
        elif head_light_flag == False:
            led.both_off()
            led_strip.colorWipe(strip, Color(0,0,0))
            if turn_sound.isPlaying():
                turn_sound.stop()

        await asyncio.sleep(100e-3) #100ms
    return

async def removetasks(loop):
    tasks = [t for t in asyncio.all_tasks() if t is not
             asyncio.current_task()]

    for task in tasks:
        # skipping over shielded coro still does not help
        if task._coro.__name__ == "cant_stop_me":
            continue
        task.cancel()

    print("Cancelling outstanding tasks")
    await asyncio.gather(*tasks, return_exceptions=True)
    loop.stop()

async def shutdown_signal(signal, loop):
    print(f"Received exit signal {signal.name}...")
    await removetasks(loop)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    strip = None
    signals = (signal.SIGHUP, signal.SIGTERM, signal.SIGINT)
    reverse_sound = SoundPlayer("/home/pi/xbox-raspberrypi-rover/soundfiles/CensorBeep.mp3", 2)        
    init_sound = SoundPlayer("/home/pi/xbox-raspberrypi-rover/soundfiles/Bleep.mp3", 2)        
    disconnect_sound = SoundPlayer("/home/pi/xbox-raspberrypi-rover/soundfiles/Disconnected.mp3", 2)        
    siren_sound = SoundPlayer("/home/pi/xbox-raspberrypi-rover/soundfiles/siren.mp3", 2)

    for s in signals:
        loop.add_signal_handler(
            s, lambda s=s: asyncio.create_task(shutdown_signal(s, loop)))
    try:
        setup()
        remote_control = connect()
        if(remote_control == None):
            print('Please connect an Xbox controller then restart the program!')
            sys.exit()        
        
        init_sound.play(1.0)

        strip = led_strip.setup_led()

        led_threading=threading.Thread(target=led_thread)     #Define a thread for ws_2812 leds
        led_threading.setDaemon(True)                         #'True' means it is a front thread,it would close when the mainloop() closes
        led_threading.start()                                 #Thread starts
    
        tasks = [remote_control.read_gamepad_input(), remote_control.rumble(), read_gamepad_inputs()]
        loop.run_until_complete(asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED))
        led.red()
        loop.run_until_complete(removetasks(loop))
        motor.destroy()
        disconnect_sound.play(1.0)
    except Exception as e:
        print("Error occured " + str(e))
    finally:
        if remote_control != None:
            remote_control.power_on = False
            #remote_control.erase_rumble()
        
        if(strip != None):
            led_strip.colorWipe(strip, Color(0,0,0))
        
        print("Closing async loop..")
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()
        led.both_off()
        GPIO.cleanup()
        print("Done..")
