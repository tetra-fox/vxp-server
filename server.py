import os
import sys
import asyncio
import websockets
from colorama import Fore, Back, Style
import updater
import processor
from logger import Logger
from config import *

logger = Logger("server", Fore.GREEN)
websocketServer = None

async def on_connect(websocket):
    await websocket.send("ayo")
    logger.log(f"Client connected. Remote address: {websocket.remote_address[0]}")

async def emit_expression(websocket):
    name = await websocket.recv()
    print(f"< {name}")

    greeting = f"Hello {name}!"

    await websocket.send(greeting)
    print(f"> {greeting}")

async def echo(websocket):
    async for message in websocket:
        logger.log(f"Received: {message}")
        await websocket.send("alive")
        logger.log(f"Sent: alive")

async def main():
    print(f"{Fore.CYAN}{Style.BRIGHT}vxp-server v{internals['Version']}", Fore.CYAN)
    print("=" * 20 + Style.RESET_ALL)
    if (not parser.getboolean("Config", "DisableUpdateCheck")): updater.check()

    clients = set()

    await processor.init()

    logger.log("Initializing...")
    
    async with websockets.serve(echo, "localhost", config["port"]) as ws:
        websocketServer = ws
        logger.ok(f"vxp-server is now reachable at ws://localhost:{config['port']}")
        await asyncio.Future()

def cleanup():
    # close any hanging threads and connections
    print("bye")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.warn("KeyboardInterrupt, shutting down gracefully...")
        cleanup()
        try:
            websocketServer.close()
            logger.ok("Server closed.")
            sys.exit(0)
        except SystemExit:
            os._exit(0)