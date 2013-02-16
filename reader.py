#!/usr/bin/env python
import serial
import os.path
import sys

SERIAL_PORT_BASE = '/dev/ttyUSB' 
MAX_PORT_ATTEMPTS = 8
BAUD_RATE = 112500
TIMEOUT = 3

NULL_READ = '---'
LEADING_DATA = 'UID: '

port_attempts = [SERIAL_PORT_BASE + str(x) for x in xrange(MAX_PORT_ATTEMPTS)]

for port in port_attempts:
    if os.path.exists(port):
        try:
            s = serial.Serial(port, BAUD_RATE, timeout=TIMEOUT)
            break
        except serial.SerialException:
            print >> sys.stderr, port + ' exists but is not readable'
            print >> sys.stderr, 'Try chmod o+r ' + port
            continue

if not s:
    print >> sys.stderr, "No USB Serial devices found"
    sys.exit()

last_uid = ''
while (True):
    line = s.readline().strip()
    if NULL_READ not in line and line != last_uid:
        print line[len(LEADING_DATA):]
        last_uid = line
