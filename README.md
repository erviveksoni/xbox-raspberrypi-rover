# Xbox Controlled Adeept Mars Rover

This repo contains a set of python scripts to drive your

[Adeept Mars Rover PiCar-B](https://www.adeept.com/adeept-mars-rover-picar-b-wifi-smart-robot-car-kit-for-raspberry-pi-3-model-b-b-2b-speech-recognition-opencv-target-tracking-stem-kit_p0117_s0030.html) with an Xbox One controller (over Bluetooth).

## Prerequisites

- [Xbox One controller](https://www.microsoft.com/en-us/p/xbox-wireless-controller/8t2d538wc7mn?cid=msft_web_collection&activetab=pivot%3aoverviewtab) Generation 2 or later which has bluetooth support
<br/>![Adeept Mars Rover PiCar-B](/images/controller.jpg)
- Pair your Xbox One Bluetooth Controller using the [xpadneo drver](https://github.com/atar-axis/xpadneo/tree/master/docs) with your Raspberry Pi (Raspbian)
- Assembled [Adeept Mars Rover PiCar-B](https://www.adeept.com/adeept-mars-rover-picar-b-wifi-smart-robot-car-kit-for-raspberry-pi-3-model-b-b-2b-speech-recognition-opencv-target-tracking-stem-kit_p0117_s0030.html)
<br/>![Adeept Mars Rover PiCar-B](/images/rover.jpg)

## Usage

* Download the Repository to your raspberry pi  
  `git clone https://github.com/erviveksoni/xbox_controller_adeept_rover.git`
* `cd xbox_controller_adeept_rover`
* Run `sudo python3 drive_rover.py`