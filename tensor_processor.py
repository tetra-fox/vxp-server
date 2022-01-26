import tensorflow as tf
import sounddevice as sd
from logger import Logger
from colorama import Fore, Back, Style

logger = Logger("processor", Fore.MAGENTA)

def init():
    # load tflite model
    logger.log("Loading model...", Fore.YELLOW)
    interpreter = tf.lite.Interpreter(model_path="models/model.tflite")
    interpreter.allocate_tensors()
    logger.ok("Model loaded.")
    
    logger.log("Initializing audio...", Fore.YELLOW)
    # stream microphone input to model
    with sd.InputStream(samplerate=16000, channels=1, callback=callback, blocksize=512):
        logger.ok("Audio initialized.")
        logger.log("Listening for input...", Fore.YELLOW)
        # wait for input
        input("Press enter to exit...")
    logger.ok("Audio initialized.")