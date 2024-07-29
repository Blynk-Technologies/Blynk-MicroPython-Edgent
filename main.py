# SPDX-FileCopyrightText: 2024 Volodymyr Shymanskyy for Blynk Technologies Inc.
# SPDX-License-Identifier: Apache-2.0
#
# This example ... TODO
# Read more: https://github.com/Blynk-Technologies/Blynk-MicroPython-Edgent
#
# The software is provided "as is", without any warranties or guarantees (explicit or implied).
# This includes no assurances about being fit for any specific purpose.

from blynk import edgent
from asyncio import sleep_ms
import logging
import board

log = logging.getLogger("app")

""" Register event handlers """

def connection_handler():
    log.info("Blynk connected")

def disconnection_handler():
    log.info("Blynk disconnected")

def data_callback(topic, payload):
    log.info("Got: %s, value: %s", topic, payload)

edgent.on_connected = connected
edgent.on_disconnected = disconnected
edgent.on_message = data_callback

""" Define asyncio tasks """

async def publisher_task():
    counter = 0
    while True:
        await sleep_ms(1000)
        edgent.publish("Counter", counter)
        counter += 1

""" Run the default asyncio loop """

edgent.run_asyncio_loop([
    publisher_task()
])
