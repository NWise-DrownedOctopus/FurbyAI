import threading
import furby_utils as utils
import server as server
import RPi.GPIO as GPIO
from pydub import AudioSegment
from pydub.playback import play
from pydub import AudioSegment
import random

############################### INTRO #################################
# Here we start up the furby's body, and have it do a short self
# introduction to the user. We are using python's threading library
# so that we can have the audio output and motor output process
# concurently.
#######################################################################
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

######################### PARROT (DEPRICATED) ##########################
# Used in showcase for high school students. Would listen for user input
# and then output pre-generated insults to mock students for interacting
# with project
########################################################################
parrot = False
while parrot == True:
	wav_file = utils.record_audio("recorded_audio.mp3", duration=5)
	utils.convert_to_mp3(wav_file, "recorded_audio.mp3")
	your_speech = utils.transcribe_audio(wav_file)
	
	if your_speech == "goodbye":
		parrot = False

	utils.synth_speech(your_speech)

	audio = AudioSegment.from_mp3("output.mp3")
	duration_seconds = len(audio) / 1000  # Convert from milliseconds to seconds

	motor_runtime = duration_seconds
	motor_start_delay = 0

	audio_thread = threading.Thread(target=play, args=(audio,))
	motor_thread = threading.Thread(target=utils.runMotorTimed, args=(motor_runtime, motor_start_delay,))

	# Start threads
	motor_thread.start()
	audio_thread.start()

	# Wait for threads to finish
	motor_thread.join()
	audio_thread.join()

	############################### INSULT #############################

	insult_num = random.randint(1, 6)

	audio = AudioSegment.from_mp3("/home/drowned0octopus/FurbyProject/" + "insult" + str(insult_num) +".mp3")
	duration_seconds = len(audio) / 1000  # Convert from milliseconds to seconds

	motor_runtime = duration_seconds
	motor_start_delay = 0

	audio_thread = threading.Thread(target=play, args=(audio,))
	motor_thread = threading.Thread(target=utils.runMotorTimed, args=(motor_runtime, motor_start_delay,))

	# Start threads
	motor_thread.start()
	audio_thread.start()

	# Wait for threads to finish
	motor_thread.join()
	audio_thread.join()


############################## USER PROMPT #############################
server.furbyConversation()
