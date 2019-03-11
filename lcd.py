from RPLCD.gpio import CharLCD
from time import sleep
import RPi.GPIO as GPIO
import bme280

button1 = 40

GPIO.setwarnings(False)

GPIO.setmode(GPIO.BOARD)
GPIO.setup(button1, GPIO.IN, pull_up_down=GPIO.PUD_UP)


#==================  LCD  ==================

leftUp = (
    0b00001,
	0b00010,
	0b00100,
	0b00100,
	0b01000,
	0b01000,
	0b10000,
	0b10000
)
leftDown = (
    0b10000,
	0b10000,
	0b01000,
	0b01000,
	0b00100,
	0b00100,
	0b00010,
	0b00001
)
rightUp = (
    0b10000,
	0b01000,
	0b00100,
	0b00100,
	0b00010,
	0b00010,
	0b00001,
	0b00001
)
rightDown = (
    0b00001,
	0b00001,
	0b00010,
	0b00010,
	0b00100,
	0b00100,
	0b01000,
	0b10000
)


def testLCD():
    lcd = CharLCD(pin_rs=15, pin_rw=None, pin_e=16, pins_data=[21, 22, 23, 24],
              numbering_mode=GPIO.BOARD,
              cols=16, rows=2, dotsize=8,
              charmap='A02',
              auto_linebreaks=False)
    lcd.write_string("TEST")


def LCDWrite():
    lcd = CharLCD(pin_rs=15, pin_rw=None, pin_e=16, pins_data=[21, 22, 23, 24],
              numbering_mode=GPIO.BOARD,
              cols=16, rows=2, dotsize=8,
              charmap='A02',
              auto_linebreaks=False)
    #
    create_chars(lcd)
              
    temperature, pressure, humidity = bme280.readBME280All()
    temperature = repr(temperature)
    pressure = repr(pressure)[:8]
    
    LCDline1 = '\x00Temp: ' + temperature + '   \x02'
    LCDline2 = '\x01Pres: ' + pressure + '\x03'

    lcd.write_string(LCDline1)
    lcd.cursor_pos = (1, 0)
    lcd.write_string(LCDline2)

    
def create_chars(lcd):
    lcd.create_char(0, leftUp)
    lcd.create_char(1, leftDown)
    lcd.create_char(2, rightUp)
    lcd.create_char(3, rightDown)


while(True):
    GPIO.wait_for_edge(button1, GPIO.FALLING)
    LCDWrite()
    sleep(0.2)

