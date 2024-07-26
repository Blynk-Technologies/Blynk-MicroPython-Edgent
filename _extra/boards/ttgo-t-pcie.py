from machine import Pin, SPI, UART
from modem import Modem
import sys, network

board_id = "TTGO T-PCIE"

# I2C
I2C_SCL = Pin(22)
I2C_SDA = Pin(21)

# Modem
MODEM_TX = Pin(27)
MODEM_RX = Pin(26)
MODEM_RST = Pin(25)
MODEM_PWRKEY = Pin(4)
MODEM_DTR = Pin(32)
MODEM_RI  = Pin(33)

# Miscelaneous
LED = Pin(12)

class Board:
    modem = None
    sta = None
    ppp = None

_board = Board()

def sta():
    if _board.sta is None:
        try:
            _board.sta = network.WLAN(network.STA_IF)
        except Exception as e:
            sys.print_exception(e)
    return _board.sta

def ppp():
    if _board.ppp is None:
        try:
            modem()
            _board.ppp = network.PPP(1)
        except Exception as e:
            sys.print_exception(e)
    return _board.ppp

def modem():
    if _board.modem is None:
        try:
            uart = UART(1, tx=MODEM_TX, rx=MODEM_RX, txbuf=2048, rxbuf=2048, timeout=100)
            _board.modem = Modem(uart=uart, rst=MODEM_RST, pwrkey=MODEM_PWRKEY)
        except Exception as e:
            sys.print_exception(e)
    return _board.modem
