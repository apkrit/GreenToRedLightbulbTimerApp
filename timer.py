# in console to install Yeelight library API for Python # pip install yeelight
# Connect Yeelight light bulb to Wifi via Yeelight App, then use Fing or any other tool to get IP of bulb. Can also retrieve via API, but this is easier for me.
import sys
import time
from yeelight import Bulb, LightType
bulb = Bulb("192.168.1.7")
red = 0
blue = 0
green = 0

def hsvTransition(lightbulb, timeAsSeconds):
    hsvColor = 130
    bulb = lightbulb
    currentTimer = timeAsSeconds
    bulb.set_brightness(5)

    interval = 130 / float(timeAsSeconds)
    for step in range(timeAsSeconds):
        bulb.set_hsv(hsvColor, 100, 100)
        hsvColor -= interval
        time.sleep(1)
        currentTimer -= 1

    time.sleep(2)
    bulb.set_rgb(0, 0, 255)
    time.sleep(1)

def greenToRedTransition(lightbulb, timeAsSeconds):
    red = 0
    green = 255
    blue = 0
    bulb = lightbulb
    currentTimer = timeAsSeconds
    bulb.set_brightness(5)

    interval = 255.0 / float(timeAsSeconds)
    for step in range(timeAsSeconds):
        if (red + interval) <= 255:
            red += interval
        else: red = 255
        if (green - interval) >= 0:
            green -= interval
        else: green = 0
        bulb.set_rgb(int(red), int(green), int(blue))
        time.sleep(1)
        print("time: " + str(currentTimer))
        print("  rgb: " + str(red) + " " + str(green) + " " + str(blue))
        currentTimer -= 1

    time.sleep(2)
    red = 255
    green = 255
    blue = 7
    bulb.set_rgb(red, green, blue)
    time.sleep(2)
        
def flashLight(lightbulb, sleepDuration, flashTimes):
    bulb = lightbulb

    bulb.start_music()
    for flash in range(flashTimes - 1): 
        bulb.set_brightness(66)
        time.sleep(sleepDuration)
        bulb.set_brightness(20)
        time.sleep(sleepDuration)
        bulb.set_brightness(66)

# Turn bulb on and set to default color, turn on music mode for streaming commands w/o limit
bulb.turn_on()
time.sleep(2)
red = 250
green = 250
blue = 7
bulb.set_rgb(red, green, blue)
bulb.set_brightness(1)

try:
    bulb.stop_music()
except Exception as e:
    pass

# Take user input for timer in minutes (or take parameter with cmd to run program ex: 'python light-timer 30' for 30 minutes
# Must be at least 1 minute
if len(sys.argv) > 1:
    userTimerInput = str(sys.argv[1])
else:
    userTimerInput = input("Enter Timer Duration in Minutes:")
    print("Timer Duration Entered: " + userTimerInput)

# On countdown start, have it turn blue and breathe through brightnesses of blue three times
# Flash blue before starting countdown
red = 0
green = 0
blue = 255
bulb.set_rgb(red, green, blue)

time.sleep(2)

flashLight(bulb, .5, 3)

time.sleep(2)

# Set color back to default color
red = 250
green = 250
blue = 7
bulb.set_rgb(red, green, blue)
bulb.set_brightness(1)

time.sleep(2)

# Then change to green before gradually changing to red over duration of timer
timeAsSeconds = int(userTimerInput) * 60
hsvTransition(bulb, timeAsSeconds)
#greenToRedTransition(bulb, timeAsSeconds) # Time as seconds is needed in order to calculate the intervals

# Turn the bulb off.
bulb.turn_off()

