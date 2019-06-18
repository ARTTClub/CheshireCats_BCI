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

lightswitch = False
previous = 0
p = false
while True:
    time.sleep(1)
    
    
    if headset.attention >= 50 and previous < 50 :
        if p ==False:
            p = True
        else:
            p = False
            print "Attention: %s" % ((headset.attention+previous)/2)
        if lightswitch == False :
            GPIO.output(17,GPIO.HIGH)
            time.sleep(1)
            lightswitch = True
        else :
            GPIO.output(17,GPIO.LOW)
            time.sleep(1)
            lightswitch = False
    previous = headset.attention    
    





