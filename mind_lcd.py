#import
import mindwave, time
import RPi.GPIO as GPIO
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
    lcd_init()
    GPIO.setup(17,GPIO.OUT)
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
        
    previous = 0   
      
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
              
        if GPIO.input(14)== GPIO.HIGH:
            
            selected = arr[i]
            print ("Selected " + selected)
            lightswitch = False
            previous = 0
            p = False
            prevAvg=0
            if i==0:
                lcd_byte(LCD_LINE_1, LCD_CMD)
                lcd_string("Sel. Attention ",2)
                time.sleep(1)
                while True:                    
                    if GPIO.input(14)==GPIO.HIGH:
                        break
                    if p == False:
                        p = True
                        previous = headset.attention
                    else:
                        p = False
                        Avg = (headset.attention+previous)/2
                        print "Attention: %s" % Avg
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
            if i ==1:
                lcd_byte(LCD_LINE_1, LCD_CMD)
                lcd_string("Sel. Meditation",2)
                time.sleep(1)
                while True:                    
                    if GPIO.input(14)==GPIO.HIGH:
                        break
                    if p == False:
                        p = True
                        previous = headset.attention
                    else:
                        p = False
                        Avg = (headset.attention+previous)/2
                        print "Meditation: %s" % Avg
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
            if i == 2:
                print('WORK IN PROGRESS')
            lcd_byte(LCD_LINE_1, LCD_CMD)
            lcd_string("-->" + arr[i],2)
            lcd_byte(LCD_LINE_2, LCD_CMD)
            lcd_string(arr[j],2)
            GPIO.output(17,GPIO.LOW)
            while GPIO.input(14)== GPIO.HIGH:
                pass
        

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


