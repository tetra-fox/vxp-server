import tensorflow as tf
import sounddevice as sd
from logger import Logger
from colorama import Fore, Back, Style

logger = Logger("processor", Fore.MAGENTA)

def init():
    logger.log("Loading model...", Fore.YELLOW)
    interpreter = tf.lite.Interpreter(model_path="models/trill.tflite")
    interpreter.allocate_tensors()
    logger.ok("Model loaded.")
    
    logger.log("Initializing audio...", Fore.YELLOW)
    # stream microphone input to model
    with sd.InputStream(samplerate=16000, channels=1, callback=callback, blocksize=512):
        logger.ok("Audio initialized.")
        logger.log("Listening for input...")
        # wait for input

def callback():
    # get input
    logger.msg("audio")
    # process input
    # send output
    pass