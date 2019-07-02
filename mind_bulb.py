#import
import mindwave, time
import RPi.GPIO as GPIO

import sys
from copy import copy
#from time import sleep, time

from lifxlan import LifxLAN


#GOTTA COMMENT
GPIO.setwarnings(False) # Ignore warning for now

# Define GPIO to LCD mapping
LCD_RS = 26
LCD_E  = 19
LCD_D4 = 13 
LCD_D5 = 6
LCD_D6 = 5
LCD_D7 = 11


# Define some device constants
LCD_WIDTH = 16    # Maximum characters per line
LCD_CHR = True
LCD_CMD = False

LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line 

# Timing constants
E_PULSE = 0.00005
E_DELAY = 0.00005


def main():
    num_lights = None
    if len(sys.argv) != 2:
        print("\nDiscovery will go much faster if you provide the number of lights on your LAN:")
        print("  python {} <number of lights on LAN>\n".format(sys.argv[0]))
    else:
        num_lights = int(sys.argv[1])

    # instantiate LifxLAN client, num_lights may be None (unknown).
    # In fact, you don't need to provide LifxLAN with the number of bulbs at all.
    # lifx = LifxLAN() works just as well. Knowing the number of bulbs in advance
    # simply makes initial bulb discovery faster.
    lifx = LifxLAN(num_lights)

    # test power control
    print("Discovering lights...")
    original_powers = lifx.get_power_all_lights()
    original_colors = lifx.get_color_all_lights()

    half_period_ms = 2500
    duration_mins = 20
    duration_secs = duration_mins*60
    print("Breathing...")
    
    #inititalize lcd display
    lcd_init()
    #GPIO.setup(23,GPIO.OUT)
    #GPIO.setup(12,GPIO.OUT)
    #GPIO.output(12,GPIO.HIGH)
    #GPIO.output(23,GPIO.HIGH)


    GPIO.setup(17,GPIO.OUT)
    #connect headset to Rpi
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
    time.sleep(1)
    # dims bulb completely at beginning
    # brightness in range [0 - 65535]
    # set_color is [Hue, Saturation, Brightness, Kelvin], duration in ms
    for bulb in original_colors:
        color = original_colors[bulb]
        dim = list(copy(color))
        dim[2] = 0
        #print "changing bulb to %s" % dim[2]
        bulb.set_color(dim, half_period_ms, rapid=True)    
    previous = 0   
    #selecting options from menu  
    arr = ['Attention', 'Meditation', 'Blink']
    i = 0
    j = 1
    lcd_byte(LCD_LINE_1, LCD_CMD)
    lcd_string('Select option',2)
    lcd_byte(LCD_LINE_2, LCD_CMD)
    lcd_string('Press any Button' ,2)
    while GPIO.input(14)==GPIO.LOW and GPIO.input(15)==GPIO.LOW:
        pass
    time.sleep(1)
    lcd_byte(LCD_LINE_1, LCD_CMD)
    lcd_string("-->" + arr[i],2)
    lcd_byte(LCD_LINE_2, LCD_CMD)
    lcd_string(arr[j],2)
    while True:
        #print "Attention: %s, Meditation: %s, previous: %s" % (headset.attention, headset.meditation,previous)
        #scroll through options on the menu
        if GPIO.input(15)== GPIO.HIGH:
            print('Scrolling--------')
            
            i = (i+1)%3
            j = (j+1)%3
            lcd_byte(LCD_LINE_1, LCD_CMD)
            lcd_string("-->" + arr[i],2)
            lcd_byte(LCD_LINE_2, LCD_CMD)
            lcd_string(arr[j],2)
            while GPIO.input(15)== GPIO.HIGH:
                pass
    ##      lcd.GPIO.cleanup()
        #select option
        if GPIO.input(14)== GPIO.HIGH:
            
            selected = arr[i]
            print ("Selected " + selected)
            lightswitch = False
            previous = []
            p = False
            prevAvg=0
            count = 0
            #if attention is selected
            if i==0:
                time.sleep(1)
                lcd_byte(LCD_LINE_2, LCD_CMD)
                lcd_string("Type end to Cont",2)
                #Take user input for number of readings per output
                avgSize =4
                while True:
                    lcd_byte(LCD_LINE_1, LCD_CMD)
                    question = "Average Size: "+str(avgSize)
                    lcd_string(question,2)
                    text = raw_input("Average Size = ")
                    if text == "end":
                        break
                    avgSize = int(text)
                    
                    
                    

                lcd_byte(LCD_LINE_1, LCD_CMD)
                lcd_string("Sel. Attention ",2)
                time.sleep(1)
                while True:                    
                    if GPIO.input(14)==GPIO.HIGH:
                        break
                    if count < avgSize-1:
                        count+=1
                        previous.append(headset.attention)
                        #for x in range(len(previous)): 
                         #   print previous[x]
                    else:
                        #p = False
                        previous.append(headset.attention)
                        #for x in range(len(previous)): 
                        #    print previous[x]
                        k = 0
                        sum = 0
                        while k < avgSize:
                            sum += previous[k]
                            k+=1
                        Avg = sum/len(previous)
                        previous = []
                        count = 0
                        print "Attention: %s" % Avg
                        #switch light state if avg is more than 50 and prev is less than 50
                        if Avg >= 50 and prevAvg < 50:
                            if lightswitch == False :
                                GPIO.output(17,GPIO.HIGH)
                                lightswitch = True
                            else:
                                GPIO.output(17,GPIO.LOW)
                                lightswitch = False
                        prevAvg = Avg
                        lcd_byte(LCD_LINE_2, LCD_CMD)
                        lcd_string(str(Avg),2)                      
                    time.sleep(1)
            #if meditation is selected
            if i ==1:
                time.sleep(1)                
                lcd_byte(LCD_LINE_2, LCD_CMD)
                lcd_string("Type end to Cont",2)
                #Take user input for number of readings per output
                avgSize =4
                while True:
                    lcd_byte(LCD_LINE_1, LCD_CMD)
                    question = "Average Size: "+str(avgSize)
                    lcd_string(question,2)
                    text = raw_input("Average Size = ")
                    if text == "end":
                        break
                    avgSize = int(text)

                lcd_byte(LCD_LINE_1, LCD_CMD)
                lcd_string("Sel. Meditation ",2)
                time.sleep(1)
                while True:                    
                    if GPIO.input(14)==GPIO.HIGH:
                        break
                    if count < avgSize-1:
                        count+=1
                        previous.append(headset.meditation)
                        #for x in range(len(previous)): 
                         #   print previous[x]
                    else:
                        #p = False
                        previous.append(headset.meditation)
                        #for x in range(len(previous)): 
                        #    print previous[x]
                        k = 0
                        sum = 0
                        while k < avgSize:
                            sum += previous[k]
                            k+=1
                        Avg = sum/len(previous)
                        #print original_colors
                        # max brightness of bulb goes from 0 to 65535 based on reverse of Avg. So closer to max meditation means dimmer bulb.
                        # brightness in range [0 - 65535]
                        # set_color is [Hue, Saturation, Brightness, Kelvin], duration in ms
                        for bulb in original_colors:
                            color = original_colors[bulb]
                            dim = list(copy(color))
                            dim[2] = 655*(100-Avg)
                            #print "changing bulb to %s" % dim[2]
                            bulb.set_color(dim, half_period_ms, rapid=True)
                        #time.sleep(half_period_ms/1000.0)
                        previous = []
                        count = 0
                        print "Meditation: %s changing bulb to %s" % (Avg,dim[2])
                        #switch light state if avg is more than 50 and prev is less than 50
                        if Avg >= 50 and prevAvg < 50:
                            if lightswitch == False :
                                GPIO.output(17,GPIO.HIGH)
                                lightswitch = True
                            else:
                                GPIO.output(17,GPIO.LOW)
                                lightswitch = False
                        prevAvg = Avg
                        lcd_byte(LCD_LINE_2, LCD_CMD)
                        lcd_string(str(Avg),2)                      
                    time.sleep(1)
            #if blink is selected
            #blink doesnt work yet
            if i == 2:
                print('WORK IN PROGRESS')
            lcd_byte(LCD_LINE_1, LCD_CMD)
            lcd_string("-->" + arr[i],2)
            lcd_byte(LCD_LINE_2, LCD_CMD)
            lcd_string(arr[j],2)
            GPIO.output(17,GPIO.LOW)
            while GPIO.input(14)== GPIO.HIGH:
                pass
        
#initialization stuff
def lcd_init():
  GPIO.setmode(GPIO.BCM)       # Use BCM GPIO numbers
  GPIO.setup(LCD_E, GPIO.OUT)  # E
  GPIO.setup(LCD_RS, GPIO.OUT) # RS
  GPIO.setup(LCD_D4, GPIO.OUT) # DB4
  GPIO.setup(LCD_D5, GPIO.OUT) # DB5
  GPIO.setup(LCD_D6, GPIO.OUT) # DB6
  GPIO.setup(LCD_D7, GPIO.OUT) # DB7

  # Initialise display
  lcd_byte(0x33,LCD_CMD)
  lcd_byte(0x32,LCD_CMD)
  lcd_byte(0x28,LCD_CMD)
  lcd_byte(0x0C,LCD_CMD)  
  lcd_byte(0x06,LCD_CMD)
  lcd_byte(0x01,LCD_CMD)
  GPIO.setwarnings(False)
##  GPIO.setup(15,GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
  GPIO.setup(14, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
  GPIO.setup(15,GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

def lcd_string(message,style):
  # Send string to display
  # style=1 Left justified
  # style=2 Centred
  # style=3 Right justified

  if style==1:
    message = message.ljust(LCD_WIDTH," ")  
  elif style==2:
    message = message.center(LCD_WIDTH," ")
  elif style==3:
    message = message.rjust(LCD_WIDTH," ")

  for i in range(LCD_WIDTH):
    lcd_byte(ord(message[i]),LCD_CHR)

def lcd_byte(bits, mode):
  # Send byte to data pins
  # bits = data
  # mode = True  for character
  #        False for command

  GPIO.output(LCD_RS, mode) # RS

  # High bits
  GPIO.output(LCD_D4, False)
  GPIO.output(LCD_D5, False)
  GPIO.output(LCD_D6, False)
  GPIO.output(LCD_D7, False)
  if bits&0x10==0x10:
    GPIO.output(LCD_D4, True)
  if bits&0x20==0x20:
    GPIO.output(LCD_D5, True)
  if bits&0x40==0x40:
    GPIO.output(LCD_D6, True)
  if bits&0x80==0x80:
    GPIO.output(LCD_D7, True)

  # Toggle 'Enable' pin
  time.sleep(E_DELAY)    
  GPIO.output(LCD_E, True)  
  time.sleep(E_PULSE)
  GPIO.output(LCD_E, False)  
  time.sleep(E_DELAY)      

  # Low bits
  GPIO.output(LCD_D4, False)
  GPIO.output(LCD_D5, False)
  GPIO.output(LCD_D6, False)
  GPIO.output(LCD_D7, False)
  if bits&0x01==0x01:
    GPIO.output(LCD_D4, True)
  if bits&0x02==0x02:
    GPIO.output(LCD_D5, True)
  if bits&0x04==0x04:
    GPIO.output(LCD_D6, True)
  if bits&0x08==0x08:
    GPIO.output(LCD_D7, True)

  # Toggle 'Enable' pin
  time.sleep(E_DELAY)    
  GPIO.output(LCD_E, True)  
  time.sleep(E_PULSE)
  GPIO.output(LCD_E, False)  
  time.sleep(E_DELAY)   

if __name__ == '__main__':
  main()



