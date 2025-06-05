import threading
import furby_utils as utils
import server as server
import RPi.GPIO as GPIO
from pydub import AudioSegment
from pydub.playback import play
from pydub import AudioSegment
import random

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)	

audio = AudioSegment.from_mp3("/home/drowned0octopus/FurbyProject/Intro1.mp3")
duration_seconds = len(audio) / 1000  # Convert from milliseconds to seconds

motor_runtime = duration_seconds
motor_start_delay = 0

# Init threads
audio_thread = threading.Thread(target=play, args=(audio,))
motor_thread = threading.Thread(target=utils.runMotorTimed, args=(motor_runtime, motor_start_delay,))

# Start threads
motor_thread.start()
audio_thread.start()

# Wait for threads to finish
motor_thread.join()
audio_thread.join()

server.furbyConversation()
