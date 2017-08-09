import RPi.GPIO as GPIO
import time
import sys
import csv

GPIO.setmode(GPIO.BCM)

#Set GPIO Pins for Trigger and Echo
TRIG = 20
ECHO = 26

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

path = "dist.csv"

def csv_writer(data, path):
    with open(path,"a", newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerow(data)

def distance():
    GPIO.output(TRIG, False)

    #print("Waiting for the sensor to settle")
    #time.sleep(2)

    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)
    
    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()
    
    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()

    pulse_length = pulse_end-pulse_start

    distance = pulse_length *17150
    distance = round(distance, 2)

    return distance

if __name__ == '__main__':
    try:
        print ("Starting Data Collection")
        print ("Storing Data to ",path)
        headers = ["Distance (cm)","Time(s)"]
        with open(path,"w", newline='') as file:
            writer = csv.writer(file, delimiter=',')
            writer.writerow(headers)
        start_time = time.time()
        while True:
            data = [distance(),time.time()-start_time]
            csv_writer(data,path)
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("Data Collection Stopped By User")
        GPIO.cleanup()
