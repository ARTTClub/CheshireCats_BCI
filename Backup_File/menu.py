import RPi.GPIO as GPIO
import sys
sys.path.append('/home/pi/lcd')
import lcd

import time
GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BCM) 
GPIO.setup(15, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 10 to be an input pin and set initial value to be pulled low (off)



count = 1

lcd.lcd_init()
lcd.lcd_byte(lcd.LCD_LINE_1, lcd.LCD_CMD)
lcd.lcd_string("Option 1", 2)
lcd.lcd_byte(lcd.LCD_LINE_2, lcd.LCD_CMD)
lcd.lcd_string("1", 2)
lcd.GPIO.cleanup()

try:
    while True:
        if GPIO.input(15) == GPIO.HIGH:
            count+=1
            if count % 3 == 1:
                lcd.lcd_byte(lcd.LCD_LINE_1, lcd.LCD_CMD)
                lcd.lcd_string("Option 1", 2)
                lcd.lcd_byte(lcd.LCD_LINE_2, lcd.LCD_CMD)
                lcd.lcd_string("1", 2)
                
            elif count % 3 == 2:
                lcd.lcd_byte(lcd.LCD_LINE_1, lcd.LCD_CMD)
                lcd.lcd_string("Option 2", 2)
                lcd.lcd_byte(lcd.LCD_LINE_2, lcd.LCD_CMD)
                lcd.lcd_string("2", 2)
              
            else:
                lcd.lcd_byte(lcd.LCD_LINE_1, lcd.LCD_CMD)
                lcd.lcd_string("Option 3", 2)
                lcd.lcd_byte(lcd.LCD_LINE_2, lcd.LCD_CMD)
                lcd.lcd_string("3", 2)
               
                             
# When you press ctrl+c, this will be called
finally:
    lcd.GPIO.cleanup()



