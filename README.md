<meta name="google-site-verification" content="PiBlIiEwdyW9Oj6LpYCuyU1cLsEYA0gSt_56QQVwhog" />
# Control a Raspberry Pi Rover using Xbox One Controller

This repo contains a set of python scripts to drive [Adeept Mars Rover PiCar-B](https://www.adeept.com/adeept-mars-rover-picar-b-wifi-smart-robot-car-kit-for-raspberry-pi-3-model-b-b-2b-speech-recognition-opencv-target-tracking-stem-kit_p0117_s0030.html) with an Xbox One controller (over Bluetooth).
The application code is not tighly coupled to work only with Adeept Mars Rover and can be easily updated to drive any Raspberry Pi enabled rover.

## Prerequisites

- Raspberry Pi (with Bluetooth)
- [Xbox One controller](https://www.microsoft.com/en-us/p/xbox-wireless-controller/8t2d538wc7mn?cid=msft_web_collection&activetab=pivot%3aoverviewtab) Generation 2 or later which has bluetooth support
<br/>![Adeept Mars Rover PiCar-B](/images/controller.jpg)
- Setup and pair your Xbox One Bluetooth Controller using the [xpadneo drver](https://github.com/atar-axis/xpadneo/tree/master/docs) with your Raspberry Pi (Raspbian)
- Assembled [Adeept Mars Rover PiCar-B](https://www.adeept.com/adeept-mars-rover-picar-b-wifi-smart-robot-car-kit-for-raspberry-pi-3-model-b-b-2b-speech-recognition-opencv-target-tracking-stem-kit_p0117_s0030.html)
<br/>![Adeept Mars Rover PiCar-B](/images/rover.jpg)

## Usage

* SSH to your raspberry pi  
* Download this Repository  
  `git clone https://github.com/erviveksoni/xbox_controller_adeept_rover.git`
* `cd xbox_controller_adeept_rover`
* Run `sudo python3 drive_rover.py`
