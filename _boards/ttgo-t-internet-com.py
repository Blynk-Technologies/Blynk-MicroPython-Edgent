from machine import Pin, SPI, UART, SDCard
from modem import Modem
import sys, network

board_id = "TTGO T-Internet-COM"

# Modem
MODEM_TX = Pin(33)
MODEM_RX = Pin(35)
MODEM_RST = Pin(32)
MODEM_PWRKEY = None

# Ethernet LAN8720
ETH_MDC = Pin(23)
ETH_MDIO = Pin(18)
ETH_PWR = Pin(4)
ETH_RST = Pin(5)
ETH_REFCLC = Pin(0)

# SPI (SDCard)
SPI_MISO = Pin(2)
SPI_MOSI = Pin(15)
SPI_CLK = Pin(14)
SD_CS = Pin(13)

# Miscelaneous
NEOPIXEL = Pin(12)
BUTTON = Pin(0, Pin.IN, Pin.PULL_UP) # Reset Button

class Board:
    modem = None
    sta = None
    lan = None
    ppp = None
    sd = None

_board = Board()

def sd():
    if _board.sd is None:
        try:
            _board.sd = SDCard(slot=2, width=1, sck=SPI_CLK, miso=SPI_MISO, mosi=SPI_MOSI, cs=SD_CS, freq=20_000_000)
        except Exception as e:
            sys.print_exception(e)
    return _board.sd

def lan():
    if _board.lan is None:
        try:
            ETH_RST.init(Pin.OUT)
            ETH_RST.value(1)
            _board.lan = network.LAN(0, phy_type=network.PHY_LAN8720,
                                     mdc=ETH_MDC, mdio=ETH_MDIO, power=ETH_PWR,
                                     ref_clk=ETH_REFCLC, ref_clk_mode=Pin.OUT, phy_addr=0)
        except Exception as e:
            sys.print_exception(e)
    return _board.lan

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
