from machine import Pin
import sys, network

board_id = "Pi Pico W"

class Board:
    sta = None

_board = Board()

def sta():
    if _board.sta is None:
        try:
            _board.sta = network.WLAN(network.STA_IF)
        except Exception as e:
            sys.print_exception(e)
    return _board.sta
