# Control a Raspberry Pi Rover using Xbox One Controller

This repo contains a set of python scripts to drive [Adeept Mars Rover PiCar-B](https://www.adeept.com/adeept-mars-rover-picar-b-wifi-smart-robot-car-kit-for-raspberry-pi-3-model-b-b-2b-speech-recognition-opencv-target-tracking-stem-kit_p0117_s0030.html) with an Xbox One controller (over Bluetooth).
The application code is not tighly coupled to work only with Adeept Mars Rover and can be easily updated to drive any Raspberry Pi enabled rover.

## Prerequisites

- Raspberry Pi (with Bluetooth)
- [Xbox One controller](https://www.microsoft.com/en-us/p/xbox-wireless-controller/8t2d538wc7mn?cid=msft_web_collection&activetab=pivot%3aoverviewtab) Generation 2 or later which has bluetooth support
<br/>![Adeept Mars Rover PiCar-B](/images/controller.jpg)
- Setup and pair your Xbox One Bluetooth Controller using the [xpadneo driver](https://github.com/atar-axis/xpadneo/tree/master/docs) with your Raspberry Pi (Raspbian)
- Assembled [Adeept Mars Rover PiCar-B](https://www.adeept.com/adeept-mars-rover-picar-b-wifi-smart-robot-car-kit-for-raspberry-pi-3-model-b-b-2b-speech-recognition-opencv-target-tracking-stem-kit_p0117_s0030.html)
<br/>![Adeept Mars Rover PiCar-B](/images/rover.jpg)
- Launch  Raspberry Pi terminal and install `sudo pip3 install evdev`

## Adding Sound Effects
The Adeept rover comes with Adafruit NeoPixel LED strip which can be used to create exciting light effects. The LED strip uses the NeoPixel library to make this work. I have realised that using this library interferes with the Raspberry Pi onboard USB and Bluetooth sound drivers. So in case you want to play some sound effects from the Raspberry then expect to hear a choppy playback.    

To workaround this, I added an external USB sound card which outputs to an 3.5mm jack connected to a small speaker. 
<br/>![USB Sound Card](/images/sound_card.jpg)

So that's on the hardware side.. Now to make it all work, I used the [SoX (Sound eXchange) python library](http://www.python-exemplary.com/index_en.php?inhalt_links=navigation_en.inc.php&inhalt_mitte=raspi/en/sound.inc.php) which can change the sound card on-the-fly and outputs the effect through the desired channel. . 
The implementation for the sound effects is done in the [Soundfile.py](https://github.com/erviveksoni/xbox-raspberrypi-rover/blob/master/soundplayer.py)

You'll need to install these packages to enable the sound effects in the code base:
`sudo apt-get install sox libsox-fmt-mp3 mp3`


## Usage

* SSH to your raspberry pi  
* Download this Repository  
  `git clone https://github.com/erviveksoni/xbox-raspberrypi-rover.git`
* `cd xbox_controller_adeept_rover`
* Run `sudo python3 drive_rover.py`
