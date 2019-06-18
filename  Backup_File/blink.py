import mindwave, time
import RPi.GPIO as GPIO

# initialise PWM pin

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(17,GPIO.OUT)

# setup headset
headset = mindwave.Headset('/dev/ttyUSB0', 'DB00')
time.sleep(2)

headset.connect()
print "Connecting..."

while headset.status != 'connected':
    time.sleep(0.5)
    if headset.status == 'standby':
        headset.connect()
        print "Retrying connect..."
print "Connected."


while True:
    time.sleep(1)
    print "Blink: %s, Meditation: %s" % (headset.blink, headset.meditation)
    if headset.blink != 0:
        print "it works"
    else:
        print ""
    