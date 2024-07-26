from machine import Pin, ADC, PWM, SPI, I2C, UART, unique_id
from modem import Modem
from pcf8563 import PCF8563
from ads1x15 import ADS1115
import sys, network, time

board_id = "Seeed EdgeBox-ESP-100"

# Digital Outputs
DO0 = Pin(40, Pin.OUT)
DO1 = Pin(39, Pin.OUT)
DO2 = Pin(38, Pin.OUT)
try:
    DO3 = Pin(37, Pin.OUT)
    DO4 = Pin(36, Pin.OUT)
    DO5 = Pin(35, Pin.OUT)
except:
    print("DO3,DO4,DO5 unavailable due to enabled Octal PSRAM")

# Digital Inputs
DI0 = Pin(4, Pin.IN)
DI1 = Pin(5, Pin.IN)
DI2 = Pin(6, Pin.IN)
DI3 = Pin(7, Pin.IN)

# Analog Outputs
AO0 = PWM(Pin(42))
AO1 = PWM(Pin(41))

# RS485
RS485_TX = Pin(17)
RS485_RX = Pin(18)
RS485_RTS = Pin(8)

# CAN
CAN_TX = Pin(1)
CAN_RX = Pin(2)

# I2C
I2C_SCL = Pin(19)
I2C_SDA = Pin(20)

I2C_ADDR_FRAM = 0x50 # FM24CL64B
I2C_ADDR_RTC  = 0x51 # PCF8563
I2C_ADDR_ECC  = 0x68 # ATECC608A
I2C_ADDR_ADC  = 0x48 # ADS1115/SGM58031

# RTC
PCF8563_INT = Pin(9, Pin.IN, Pin.PULL_UP)

# Modem A7670G-LABE
MODEM_TX = Pin(48)
MODEM_RX = Pin(47)
MODEM_RST = Pin(16)     # Enable power through SY8089A
MODEM_PWRKEY = Pin(21)

# SPI (Ethernet)
SPI_MISO = Pin(11)
SPI_MOSI = Pin(12)
SPI_CLK = Pin(13)

# Ethernet W5500
ETH_CS  = Pin(10)
ETH_INT = Pin(14)
ETH_RST = Pin(15)

# Miscelaneous
LED = Pin(43) # Same as TX
LED_ERR = Pin(44) # Same as RX
BUZZER = Pin(45) # Buzzer (active high)
BUTTON = Pin(0, Pin.IN, Pin.PULL_UP) # Reset Button

class Board:
    spi = None
    i2c = None
    rs485 = None
    modem = None
    sta = None
    lan = None
    ppp = None
    rtc = None
    adc1 = None
    fram = None

_board = Board()


class I2CMemDev:
    def __init__(self, i2c:I2C, address, block_size, block_count, addrsize=16):
        self.i2c = i2c
        self.addr = address
        self.addrsize = addrsize
        self.block_size = block_size
        self.block_count = block_count

    def readblocks(self, block_num, buf, offset=0):
        memaddr = block_num * self.block_size + offset
        self.i2c.readfrom_mem_into(self.addr, memaddr, buf, addrsize=self.addrsize)

    def writeblocks(self, block_num, buf, offset=0):
        memaddr = block_num * self.block_size + offset
        self.i2c.writeto_mem(self.addr, memaddr, buf, addrsize=self.addrsize)

    def ioctl(self, op, arg):
        if op == 4:
            return self.block_count
        if op == 5:
            return self.block_size
        if op == 6: # block erase
            return 0

def i2c():
    if _board.i2c is None:
        try:
            _board.i2c = I2C(1, scl=I2C_SCL, sda=I2C_SDA, freq=400_000)
        except Exception as e:
            sys.print_exception(e)
    return _board.i2c

def spi():
    if _board.spi is None:
        try:
            _board.spi = SPI(2, sck=SPI_CLK, mosi=SPI_MOSI, miso=SPI_MISO, baudrate=40_000_000)
        except Exception as e:
            sys.print_exception(e)
    return _board.spi

def rtc():
    if _board.rtc is None:
        try:
            _board.rtc = PCF8563(i2c(), I2C_ADDR_RTC)
        except Exception as e:
            sys.print_exception(e)
    return _board.rtc

def adc1():
    if _board.adc1 is None:
        try:
            _board.adc1 = ADS1115(i2c(), I2C_ADDR_ADC)
        except Exception as e:
            sys.print_exception(e)
    return _board.adc1

def fram():
    if _board.fram is None:
        try:
            _board.fram = I2CMemDev(i2c(), I2C_ADDR_FRAM, 128, 8192 // 128, 16)
        except Exception as e:
            sys.print_exception(e)
    return _board.fram

def lan():
    if _board.lan is None:
        try:
            _board.lan = network.LAN(0, phy_type=network.PHY_W5500, spi=spi(),
                                     phy_addr=1, cs=ETH_CS, int=ETH_INT)
            mac = bytearray(unique_id())[:6]
            mac[5] = (mac[5] + 4) % 255
            _board.lan.config(mac=mac)
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
            m = modem()
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

def rs485():
    if _board.rs485 is None:
        try:
            _board.rs485 = UART(2, tx=RS485_TX, rx=RS485_RX, rts=RS485_RTS, txbuf=2048, rxbuf=2048, timeout=100)
        except Exception as e:
            sys.print_exception(e)
    return _board.rs485

def beep(dur=100):
    BUZZER.init(Pin.OUT)
    BUZZER.on()
    time.sleep_ms(dur)
    BUZZER.off()
