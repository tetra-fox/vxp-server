import tensorflow as tf
import pyaudio
import wave
import numpy as np
import time
import threading
import queue
import os
import sys
import json
import base64
from logger import Logger
from colorama import Fore, Back, Style

LoggerInstance = Logger("processor", Fore.MAGENTA)

def init():
    # load tflite model
    LoggerInstance.log("Loading model...", Fore.YELLOW)
    interpreter = tf.lite.Interpreter(model_path="models/model.tflite")
    interpreter.allocate_tensors()
    LoggerInstance.log("Model loaded.", Fore.GREEN)
    
    LoggerInstance.log("Initializing audio...", Fore.YELLOW)
    # stream microphone input to model
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)
    stream.start_stream()
    LoggerInstance.log("Audio initialized.", Fore.GREEN)

    # decode audio