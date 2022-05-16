# -*- coding: utf-8 -*-
"""
This program is used to load the data from the USB serial.
 Whenever the serial port receives data, it will be placed in
 the "line" variable. From here, it needs to be parsed and saved.
 
You can enable a "development" mode which will feed fake data 
 by setting dev = True
"""
import matplotlib.pyplot as plt
import serial
import time
from IAC_helper import port_scan, development_data
import pandas as pd
import re

running = True
calibrating = True
dev = True  # Development mode
usbPort = "COM3"  # Your USB port, obtain using port_scan()
reference_weight = input("Enter reference weight (N):")
Fref = [0, float(reference_weight)]
LF = []
P1 = []
I1 = []
LL = []
P2 = []
I2 = []
xtab1 = []
ytab1 = []
xtab2 = []
ytab2 = []
SD1 = []
SD2 = []
L = 0
F = 0
x = 0
deltatime = []
time1 = 0
timedata = []

try:
    if not dev:
        ser = serial.Serial(usbPort, 9600)
    print("Serial initialized succesfully!")
except:
    print("Issue with serial! Aborting...")


def splitfl(k, place):
    numbers = []
    for t in line.split():
        if t.lstrip('-').isnumeric() or t.isnumeric():  # takes into account for - numbers
            numbers.append(t)
    k.append(float(numbers[place]))  # takes out the numbers of the string


def splitint(j, place):
    numbers = []
    for t in line.split():
        if t.lstrip('-').isnumeric() or t.isnumeric():  # takes into account for - numbers

            numbers.append(t)
    j.append(float(numbers[place]))  # takes out the numbers of the string


def splitc(h, g, f, place):
    numbers = []
    for t in line.split():
        if t.lstrip('-').isnumeric() or t.isnumeric():  # takes into account for - numbers
            numbers.append(t)
    F = g * float(numbers[place]) + f
    h.append(F)  # takes out the numbers of the string


def plot(f, x1, x2, leg):
    plt.title(f)
    plt.xlabel(x1)
    plt.ylabel(x2)
    plt.legend(leg)
    plt.show()

if dev:
    currentTime = time.time()
    while calibrating:
        # Delay 1 second
        while currentTime + 1 > time.time():
            pass
        currentTime = time.time()

        test1 = input('Press Enter to start calibrating 0 value')
        if test1 == "":
            test1 = True
        test2 = False
        log = False
        Layer = 0
        while test1:
            line = development_data()[:-2].decode('utf-8')
            splitfl(I1, 0)
            line = development_data()[1:].decode('utf-8')
            splitfl(I2, 1)
            if len(I2) >= 10:
                F0 = sum(I1[0:]) / 10  # averages the 10 results and saves it for
                L0 = sum(I2[0:]) / 10  # further calculations
                test1 = False

        test2 = input('Press Enter to start calibrating 1 value')
        if test2 == "":
            test2 = True
            Lref0 = float(input('Enter starting height (mm):'))
        test1 = False
        log = False

        while test2:
            line = development_data()[:-2].decode('utf-8')
            splitint(P1, 0)
            line = development_data()[1:].decode('utf-8')
            splitint(P2, 1)
            if len(P2) >= 10:
                F1 = sum(P1[0:]) / 10
                L1 = sum(P2[0:]) / 10
                test2 = False

        Lref1 = float(input('Enter ending height (mm):'))
        a1 = (Fref[1] - Fref[0]) / (F1 - F0)
        b1 = Fref[1]
        a2 = (Lref0 - Lref1) / (L1 - L0)
        b2 = 0
        calibrating = False

    while running:
        # Delay 1 second
        while currentTime + 1 > time.time():
            pass
        currentTime = time.time()

        log = input('Press Enter to start logging data')

        if log == "":
            log = True
        test2 = False
        test1 = False
        tme = time.time()

        while log:

            time.sleep(0.01)

            time0 = tme
            tme = time.time()
            elapsed = tme - time0
            deltatime.append(float(elapsed))

            line = development_data()[:-2].decode('utf-8')
            splitc(LF, a1, b1, 0)
            line = development_data()[:-2].decode('utf-8')
            splitc(SD1, 1, 0, 0)

            line = development_data()[1:].decode('utf-8')
            splitc(LL, a2, b2, 1)

            line = development_data()[1:].decode('utf-8')
            splitc(SD2, 1, 0, 1)


            if len(LL) >= 100:
                running = False
                log = False
                for i in deltatime:
                    timedata.append(time1)
                    time1 += i
                print(timedata)

else:

    while calibrating:
        test1 = input('Press Enter to start calibrating 0 value')

        if test1 == "":
            test1 = True

        test2 = False
        log = False
        Layer = 0

        while test1:
            line = ser.readline()[:-2].decode('utf-8')
            splitfl(I1)
            line = ser.readline()[1:].decode('utf-8')
            splitfl(I2)
            if len(I2) >= 10:
                F0 = sum(I1[0:]) / 10
                L0 = sum(I2[0:]) / 10
                test1 = False

        test2 = input('Press Enter to start calibrating 1 value')

        if test2 == "":
            test2 = True
            Lref0 = float(input('Enter starting height (mm):'))

        test1 = False
        log = False

        while test2:

            line = ser.readline()[:-2].decode('utf-8')
            splitint(P1, 0)

            line = ser.readline()[1:].decode('utf-8')
            splitint(P2, 1)

            if len(P2) >= 10:
                F1 = sum(P1[0:]) / 10
                L1 = sum(P2[0:]) / 10
                test2 = False

        Lref1 = float(input('Enter ending height (mm):'))
        a1 = (Fref[1] - Fref[0]) / (F1 - F0)
        b1 = Fref[1]
        a2 = (Lref0 - Lref1) / (L1 - L0)
        b2 = 0
        calibrating = False

    while running:

        log = input('Press Enter to start logging data')

        if log == "":
            log = True
        test2 = False
        test1 = False
        tme = time.time()
        while log:

            line = ser.readline()[:-2].decode('utf-8')
            splitc(LF, a1, b1, 0)

            line = ser.readline()[:-2].decode('utf-8')
            splitc(SD1, 1, 0, 0)

            line = ser.readline()[1:].decode('utf-8')
            splitc(LL, a2, b2, 1)

            line = ser.readline()[1:].decode('utf-8')
            splitc(SD2, 1, 0, 1)

            time0 = tme
            tme = time.time()
            elapsed = tme - time0
            deltatime.append(elapsed)

            if input() == '':
                Stop = True


            if Stop:
                running = False
                log = False
                for i in deltatime:
                    timedata.append(time1)
                    time1 += float(i)



ytab1 = LF
ytab2 = LL



col1 = "Time (s)"
col2 = "Sensor data distance"
col3 = "Sensor data force"
col4 = "Force (N)"
col5 = "Displacement (mm)"

data = pd.DataFrame({col1: timedata, col2: SD1, col3: SD2, col4: LF, col5: LL})
data.to_excel('Sensor data.xlsx', sheet_name='sheet1', index=False)

f1 = open('Calibrating_data.txt', 'w')
f1.write('a Force: ' + str(a1) + '\n')
f1.write('b Force: ' + str(b1) + '\n')
f1.write('a Distance: ' + str(a2)+ '\n')
f1.write('b Distance: ' + str(b2)+ '\n')
f1.write('Reference weight: ' + str(reference_weight)+ 'N \n')
f1.write('Reference distance: ' + str(Lref1) + 'mm \n')
f1.close()

plt.plot(timedata, ytab1)
plot('F(t)', 't (s)', 'F (N)', 'Force')

plt.plot(timedata, ytab2)
plot('L(t)', 't (s)', 'L (mm)', 'Displacement')
