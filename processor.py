import tensorflow as tf
from tensorflow import keras
import sounddevice as sd
from logger import Logger
from colorama import Fore, Back, Style
import numpy as np
import asyncio
from config import *
import tensorflow_hub as hub

logger = Logger("processor", Fore.MAGENTA)

interpreter = None

async def init():
    
    logger.warn("Loading model...")
    global interpreter
    interpreter = tf.lite.Interpreter(model_path=internals['modelpath'])
    logger.ok("Model loaded.")
    
    logger.warn("Initializing audio...")
    default_input_device = sd.query_devices(kind="input")
    logger.log(f"Using default input device: {default_input_device['name']}")
    
    # begin listening & interpreting
    await record_buffer()

async def record_buffer():
    event = asyncio.Event()

    def callback(data, frames, time, status):
        # print(status)

        # Run inference with TFLite model.
        input_details = interpreter.get_input_details()
        interpreter.resize_tensor_input(input_details[0]["index"], data.shape)
        interpreter.allocate_tensors()
        interpreter.set_tensor(input_details[0]["index"], data)
        interpreter.invoke()

        module = hub.KerasLayer('https://tfhub.dev/google/nonsemantic-speech-benchmark/trill-distilled/3')
        module.predict(data)


        # Get TFLite output.
        output_data = interpreter.get_tensor(interpreter.get_output_details()[0]["index"])
        bruh = model.predict(output_data)
        print(bruh)
        # logger.log(output_data)


    stream = sd.InputStream(samplerate=16000, channels=1, callback=callback, blocksize=32000)

    with stream:
        await event.wait()

