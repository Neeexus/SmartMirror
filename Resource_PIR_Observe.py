

import RPi.GPIO as GPIO
from coapthon.resources.resource import Resource
import threading
import logging as logger
import week10_lcd_driver
import RPi.GPIO as GPIO
from datetime import datetime

import Adafruit_DHT
from time import *

PIN_BTN = 17
PIN_LED = 22
ASSISTANT = None

sensor=Adafruit_DHT.DHT11
pin=14

lcd=week10_lcd_driver.lcd()
lcd.lcd_clear()



class ObservableResource(Resource):
    def __init__(self, name="Obs", coap_server=None):
        super(ObservableResource, self).__init__(name, coap_server, visible=True, observable=True, allow_children=False)
        self.payload = True
        self.period = 10
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(26, GPIO.IN)
        self.update(True)


    def render_GET(self, request):
        if self.payload!=GPIO.input(26):
            self.payload=str("Hello there")
        else:
            self.payload=str(datetime.now())
        
        return self
    def redern_PUT(self, request):
        return self
    def render_POST(self, request):
        self.payload = request.payload
        return self

    def render_DELETE(self, request):
        return True

    def update(self, first=False):
        if not self._coap_server.stopped.isSet():
            timer = threading.Timer(self.period, self.update)
            timer.setDaemon(True)
            timer.start()

            if not first and self._coap_server is not None:
                temp_value = GPIO.input(26)
                if self.payload != GPIO.input(26):
                    
                    lcd.lcd_clear()
                    lcd.lcd_display_string("Detected",1)
                     
                    logger.debug("Value CHANGED")
                    sleep(1)
                    i=0
                    while i<4:    
                        now=localtime()
                        dt="%04d-%02d-%02d" %(now.tm_year, now.tm_mon, now.tm_mday)
                        tt="%02d:%02d-%02d" %(now.tm_hour, now.tm_min, now.tm_sec)
                        lcd.lcd_display_string(dt, 1)
                        lcd.lcd_display_string(tt, 2)
                        sleep(1)
                        lcd.lcd_clear()
                        i+=1
                    h,t=Adafruit_DHT.read_retry(sensor,pin)
                    if h is not None and t is not None:
                        lcd.lcd_display_string("Temp={0:0.1f}C".format(t,h),1)
                        lcd.lcd_display_string("Hum={1:0.1f}%".format(t,h),2)
                    else:
                        lcd.lcd_display_string("Read error",1)
                    sleep(3)
                    lcd.lcd_clear()
                    
                    self.payload = temp_value
                    self._coap_server.notify(self)
                    self.observe_count += 1
                   
                    
                  
                    
                else:
                    lcd.lcd_clear()
                    lcd.lcd_display_string("Not Detected",1)
                    logger.debug("Value Not CHANGED")
                    sleep(2)
                    self.payload = temp_value
                    self._coap_server.notify(self)
                    self.observe_count += 1
   
    
