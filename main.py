# This example bla bla bla
# Read detailed explanations here:
#   https://docs.blynk.io/bla-bla-bla

from blynk import mqtt, edgent
from asyncio import sleep_ms
import logging, board

log = logging.getLogger("app")

""" Register event handlers """

@edgent.on(edgent.CONNECTED)
def connected_handler():
    log.info("MQTT connected")

@edgent.on(edgent.DISCONNECTED)
def disconnected_handler():
    log.info("MQTT disconnected")

@edgent.on_message("ds/LED")
def led_handler(data):
    if hasattr(board, "LED"):
        board.LED.write(int(data))
    else:
        log.info("Your LED is %s", data)

@edgent.on_message()  # Handle all other messages
def other_handler(topic, payload):
    log.info("Got: %s, value: %s", topic, payload)

""" Define our asyncio tasks """

async def publisher_task():
    counter = 0
    while True:
        await sleep_ms(1000)
        try:
            mqtt.publish("ds/Counter", counter)
            counter += 1
        except Exception as e:
            pass

""" Run the default asyncio loop """

edgent.run_asyncio_loop([
    publisher_task()
])
