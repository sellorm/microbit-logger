#!/usr/bin/env python3
import datetime
import serial
import serial.tools.list_ports as list_ports
import sqlite3


PID_MICROBIT = 516
VID_MICROBIT = 3368
TIMEOUT = 0.1


def find_comport(pid, vid, baud):
    ''' return a serial port '''
    ser_port = serial.Serial(timeout=TIMEOUT)
    ser_port.baudrate = baud
    ports = list(list_ports.comports())
    print('scanning ports')
    for p in ports:
        print('port: {}'.format(p))
        try:
            print('pid: {} vid: {}'.format(p.pid, p.vid))
        except AttributeError:
            continue
        if (p.pid == pid) and (p.vid == vid):
            print('found target device pid: {} vid: {} port: {}'.format(
                p.pid, p.vid, p.device))
            ser_port.port = str(p.device)
            return ser_port
    return None


def main():
    print('looking for microbit')
    ser_micro = find_comport(PID_MICROBIT, VID_MICROBIT, 115200)
    if not ser_micro:
        print('microbit not found')
        return
    print('opening and monitoring microbit port')
    ser_micro.open()
    while True:
        line = ser_micro.readline().decode('utf-8')
        if line:  # If it isn't a blank line
            response = line.strip().split(',')

            print('Timestamp: {:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()))
            print('temperature: {}\nlight: {}'.format(response[0], response[1]))
            conn = sqlite3.connect('microbit-logger.db')
            c = conn.cursor()

            # Insert a row of data
            c.execute("INSERT INTO logger VALUES (date(),time(),?,?)", (response[0],response[1]))

            # Save (commit) the changes
            conn.commit()

            # We can also close the connection if we are done with it.
            # Just be sure any changes have been committed or they will be lost.
            conn.close()
            
            
    ser_micro.close()

if __name__ == "__main__":
  main()

