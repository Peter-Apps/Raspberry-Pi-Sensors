import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

GPIO.setup(4,GPIO.IN)

start = time.time()
stop = time.time()
gateState = False
mid = 0


try:
        while True:
                # gateState is True if sensor is tripped
                if (GPIO.input(4) != gateState):
                        gateState = not gateState

                        if (gateState == True):
                                start = time.time()
                        else:
                                stop = time.time()

                        if stop - start > 0.01:
                                print "Time: ", stop - start, "s"
                                print "speed: ", 0.04/(stop - start), "m/s"
                                print "Period: ", ((start + stop)/2 - mid)*2, "s"
                                print "  "

                                mid = (start + stop)/2

except KeyboardInterrupt:
    GPIO.cleanup()
            


                
