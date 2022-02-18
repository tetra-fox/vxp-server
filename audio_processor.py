import tensorflow as tf
from tensorflow import keras
from logger import Logger
from colorama import Fore, Back, Style
import numpy as np
import asyncio
from config import *
import tensorflow_hub as hub
from scipy.signal.signaltools import wiener
import keras as K
import wave
from array import array
import struct
import time
import os
from json_tricks import load

import numpy as np

import librosa
from pydub import AudioSegment, effects
import noisereduce as nr

import tensorflow as tf
import keras
from keras.models import model_from_json
from keras.models import load_model
from scipy.io.wavfile import write

import matplotlib.pyplot as plt

logger = Logger("processor", Fore.MAGENTA)
interpreter = None
model = None

# Label mappings (indexes correspond to the model's output tensor)

emotions = {
    0: "neutral",
    1: "calm",
    2: "happy",
    3: "sad",
    4: "angry",
    5: "fearful",
    6: "disgust",
    7: "suprised"
}

savee_emojis = {"neutral": "😐", "calm": "😌", "happy": "😊", "sad": "😢",
                "angry": "😡", "fearful": "😱", "disgust": "🤮", "suprised": "😲"}

RATE = 24414
CHUNK = 512
RECORD_SECONDS = 7.1
CHANNELS = 1
WAVE_OUTPUT_FILE = "./cache/buffer.wav"

assert tf.executing_eagerly()

# I really don't know what I'm doing here lol
# I've never touched ML or NNs before, but here we go
# Also this is the first real independent project I've done in Python lol


async def init():
    logger.warn("Loading model...")
    global interpreter
    global model

    with open(internals["modelpath"], "r") as json_file:
        json_savedModel = json_file.read()

    model = tf.keras.models.model_from_json(json_savedModel)
    model.load_weights(internals["weightspath"])

    model.compile(loss="categorical_crossentropy",
                  optimizer="RMSProp",
                  metrics=["categorical_accuracy"])

    print(model.summary())

    logger.ok("Model loaded.")

    logger.warn("Initializing audio...")
    import sounddevice as sd
    default_input_device = sd.query_devices(kind="input")
    logger.log(f"Using default input device: {default_input_device['name']}")

    await record_buffer()

    # # begin listening & interpreting
    # record_buffer()


async def record_buffer():
    import sounddevice as sd
    event = asyncio.Event()

    def callback(data, frames, time, status):

        print("* recording...")
        write(WAVE_OUTPUT_FILE, RATE, np.array(data, dtype=np.int32))
        print("* done recording")

        x = preprocess(WAVE_OUTPUT_FILE)
        # Model's prediction => an 8 emotion probabilities array.

        predictions = model.predict(x, use_multiprocessing=True)
        pred_list = list(predictions)

        # Get rid of 'array' & 'dtype' statments.
        pred_np = np.squeeze(np.array(pred_list).tolist(), axis=0)

        max_emo = np.argmax(predictions)
        print("max emotion:", emotions.get(max_emo, -1))

        print(100*"-")

    stream = sd.InputStream(samplerate=RATE, channels=CHANNELS,
                            callback=callback, blocksize=CHUNK, dtype=np.int32)

    with stream:
        await event.wait()


def preprocess(file_path, frame_length=2048, hop_length=512):
    # Fetch sample rate.
    _, sr = librosa.load(path=file_path, sr=None)
    # Load audio file
    rawsound = AudioSegment.from_file(file_path, duration=None)
    # Normalize to 5 dBFS
    normalizedsound = effects.normalize(rawsound, headroom=5.0)
    # Transform the audio file to np.array of samples
    normal_x = np.array(normalizedsound.get_array_of_samples(),
                        dtype=np.float32)
    # Noise reduction
    final_x = nr.reduce_noise(y=normal_x,  y_noise=normal_x, sr=sr)

    rms = librosa.feature.rms(final_x, frame_length=frame_length, hop_length=hop_length,
                              center=True, pad_mode='reflect').T 
    zcr = librosa.feature.zero_crossing_rate(
        final_x, frame_length=frame_length, hop_length=hop_length, center=True).T

    mfcc = librosa.feature.mfcc(final_x, sr=sr, S=None,
                                n_mfcc=13, hop_length=hop_length).T

    X = np.concatenate((rms, zcr, mfcc), axis=1)

    X_3D = np.expand_dims(X, axis=0)

    return X_3D
