
from time import sleep

from coapthon.resources.resource import Resource
from datetime import datetime
import threading
import logging as logger

import Adafruit_DHT
import RPi.GPIO as gp
PIN_BTN = 17
PIN_LED = 22
ASSISTANT = None
gp.setmode(gp.BCM)


gp.setmode(gp.BCM)
sensor=Adafruit_DHT.DHT11
gp.setwarnings(False)
pin=14
gp.setup(6,gp.OUT)
gp.setup(13,gp.OUT)
gp.setup(19,gp.OUT)

gp.output(6,False)
gp.output(13,False)
gp.output(19,False)

class TimeResource(Resource):
    def __init__(self, name="BasicResource", coap_server=None):
        super(TimeResource, self).__init__(name, coap_server, visible=True,
                                            observable=True, allow_children=True)
        self.payload = str(datetime.now())

    def render_GET(self, request):
        h,t=Adafruit_DHT.read_retry(sensor,pin)
            
        self.payload=request.payload
        if t is not None and h is not None:
            temp=str('{0:0.1f}'.format(t))
            if  str(self.payload)<temp:
                gp.output(6,True)
                gp.output(13,False)
                gp.output(19,False)
                sleep(2)
                self.payload=str("희망온도: "+request.payload+"현재온도: "+temp+"냉방을 시작합니다..")
            elif str(self.payload)==temp:
                gp.output(6,False)
                gp.output(13,True)
                gp.output(19,False)
                sleep(2)
                self.payload=str("희망온도: "+request.payload+"현재온도: "+temp+"보일러 작동을 중지합니다..")
            else:    
                gp.output(6,False)
                gp.output(13,False)
                gp.output(19,True)
                sleep(2)
                self.payload=str("희망온도: "+request.payload+"현재온도: "+temp+"보일러 작동을 시작합니다..")                
        gp.output(6,False)
        gp.output(13,False)
        gp.output(19,False)
           
                    
        return self
    def render_PUT(self, request):
        self.payload = request.payload
        return self

    def render_POST(self, request):
        res = TimeResource()
        res.location_query = request.uri_query
        res.payload = request.payload
        return res

    def render_DELETE(self, request):
        return True


class ObservableResource(Resource):
    def __init__(self, name="Obs", coap_server=None):
        super(ObservableResource, self).__init__(name, coap_server, visible=True, observable=True, allow_children=False)
        self.payload=self
        self.period = 10
        self.update(True)

    def render_GET(self, request):
      
        h,t=Adafruit_DHT.read_retry(sensor,pin)

        if h is not None and t is not None:
            self.payload=str("Temp={0:0.1f}C".format(t,h)+",Hum={1:0.1f}%".format(t,h))
        else:
            self.payload=str("Read error")

        return self

    def render_POST(self, request):
        str(self.payload)
        return self
    def render_PUT(self, request):

        return self
    def render_DELETE(self, request):
        return True


    def update(self, first=False):
       
        if not self._coap_server.stopped.isSet():
            timer = threading.Timer(self.period, self.update)
            timer.setDaemon(True)
            timer.start()

            if not first and self._coap_server is not None:
                logger.debug("Periodic Update")
                self._coap_server.notify(self)
                self.observe_count += 1