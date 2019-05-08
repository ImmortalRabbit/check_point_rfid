# check_point_rfid
A small project on arduino that can give an access for certain user to light lamp.

Used:
* Arduino
* Python3
* Postgresql

Python3 Libraries:
psycopg2
tkinter

Arduino Libraries:
rfid2

Circuit:
RFID -> Arduino Mega
VCC  -> 3.3V
RST  -> 2 pin
GND -> GND
MISO -> 3
MOSI -> 4
SCK -> 5
NSS -> 6
IRQ -> 7

Relay -> Arduino Mega
VCC -> 5.0V
IN -> 10 pin
GND -> GND

Relay  -> Lamp's wire
COM -> first part
NO -> second part
