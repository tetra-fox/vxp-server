import tensorflow as tf
from tensorflow import keras
import sounddevice as sd
from logger import Logger
from colorama import Fore, Back, Style
import numpy as np
import asyncio
from config import *
import tensorflow_hub as hub
from scipy.signal.signaltools import wiener
# from predict_emotion_tf import *

logger = Logger("processor", Fore.MAGENTA)
interpreter = None
emotions_ravdess = ['neutral', 'calm', 'happy',
                    'sad', 'angry', 'fearful', 'disgust', 'surprised']
emoji_dict = {"neutral": "😐", "calm": "😌", "happy": "😊", "sad": "😢",
              "angry": "😡",  "fearful": "😱", "disgust": "🤮", "surprised": "😲"}

# I really don't know what I'm doing here lol
# I've never touched ML or TF before

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
        # ser_trill_model_ravdess = TRILLSERModel(SER_TRILL_MODEL_RAVDESS, TRILL_URL, emotions_ravdess, input_length_ravdess, SAMPLING_RATE)
        # ser_trill_model_ravdess.predict_emotion(data)

        # return

        # Run inference with TFLite model.
        input_details = interpreter.get_input_details()
        output_details = interpreter.get_output_details()

        # model_input = np.zeros([1, 32000], dtype=np.float32)

        interpreter.resize_tensor_input(input_details[0]["index"], data.shape)
        interpreter.allocate_tensors()
        interpreter.set_tensor(input_details[0]["index"], data)
        interpreter.invoke()

        # Get TFLite output.
        output_data = interpreter.get_tensor(output_details[0]["index"])

        prediction = emotions_ravdess[np.argmax(
            output_data) % len(emotions_ravdess)]

        logger.log(prediction + emoji_dict[prediction])
        # logger.log(output_data)

    stream = sd.InputStream(samplerate=16000, channels=1,
                            callback=callback, blocksize=16382)

    with stream:
        await event.wait()
