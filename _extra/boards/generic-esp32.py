from machine import Pin, RTC
import sys, network

board_id = "Generic ESP32"

class Board:
    sta = None
    rtc = None

_board = Board()

def rtc():
    if _board.rtc is None:
        try:
            _board.rtc = RTC()
        except Exception as e:
            sys.print_exception(e)
    return _board.rtc

def sta():
    if _board.sta is None:
        try:
            _board.sta = network.WLAN(network.STA_IF)
        except Exception as e:
            sys.print_exception(e)
    return _board.sta
