import asyncio
from logger import Logger
import websockets
# import tensor_processor as tp
import requests
import semver
from config import *
import sys
import os
from colorama import Fore, Back, Style
from logger import Logger
import updater
import enum

LoggerInstance = Logger("server", Fore.GREEN)

async def on_connect(websocket):
    await websocket.send("ayo")
    LoggerInstance.log("Client connected.")

async def emit_expression(websocket):
    name = await websocket.recv()
    print(f"< {name}")

    greeting = f"Hello {name}!"

    await websocket.send(greeting)
    print(f"> {greeting}")

def main():
    print(f"{Fore.CYAN}{Style.BRIGHT}vxp-server v{internals['Version']}", Fore.CYAN)
    print("=" * 20 + Style.RESET_ALL)
    if (not parser.getboolean("Config", "DisableUpdateCheck")): updater.check()

    # tp.init()
    
    start_server = websockets.serve(on_connect, "localhost", config['Port'])

    asyncio.get_event_loop().run_until_complete(start_server)
    LoggerInstance.ok(f"vxp-server is now reachable at ws://localhost:{config['Port']}")
    
    asyncio.get_event_loop().run_forever()

def cleanup():
    # close any hanging threads and connections
    print("bye")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        LoggerInstance.warn("KeyboardInterrupt, shutting down gracefully...")
        cleanup()
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)