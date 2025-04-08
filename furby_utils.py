import RPi.GPIO as GPIO
import time
import io
import os
import pyaudio
from pydub import AudioSegment
import wave
from google.cloud import texttospeech as tts
from google.cloud import speech

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/drowned0octopus/FurbyProject/furbyproject-714197248f2d.json"

def runMotorTimed(rtime, startDelay):
	# Trying to run motor for set durationg
	runTime = rtime

	GPIO.setup(26, GPIO.OUT, initial=GPIO.LOW)
	
	# Here we should flip the swith, wait the amount of time, and then flip the switch again
	time.sleep(startDelay)
	GPIO.output(26,True)
	time.sleep(runTime)

	GPIO.output(26,False)
	
def powerGPIOheadTimed(rtime, GPIOhead):
	# Trying to run motor for set durationg
	runTime = rtime

	GPIO.setup(GPIOhead, GPIO.OUT, initial=GPIO.LOW)
	
	GPIO.output(GPIOhead,True)
	time.sleep(runTime)

	GPIO.output(GPIOhead,False)
	
def detectSensor(rtime):
	runTime = rtime
	
	GPIO.setup(16, GPIO.IN)
	count = 0;
	
	while count < runTime:
		sensorValue = GPIO.input(16)
			
		print(f"Sensor Value: {sensorValue}")
		time.sleep(1)
		count += 1

def synth_speech(text, file_name = "output.mp3"):
	client = tts.TextToSpeechClient()
	synthesis_input = tts.SynthesisInput(text=text)
	
	voice = tts.VoiceSelectionParams(
		language_code = "en_US",
		ssml_gender=tts.SsmlVoiceGender.NEUTRAL,
	)
	
	audio_config = tts.AudioConfig(
		audio_encoding=tts.AudioEncoding.MP3
	)
	
	response = client.synthesize_speech(
		input=synthesis_input, voice=voice, audio_config=audio_config
	)
	
	with open(file_name, "wb") as out:
		out.write(response.audio_content)
		print("Audio content written to " + file_name)
		
def record_audio(filename, duration=5, rate=44100, channels=1, chunk=1024):
    p = pyaudio.PyAudio()
    
    stream = p.open(format=pyaudio.paInt16,
                    channels=channels,
                    rate=rate,
                    input=True,
                    frames_per_buffer=chunk)
    
    print(f"Recording for {duration} seconds...")
    frames = []
    
    for _ in range(0, int(rate / chunk * duration)):
        data = stream.read(chunk)
        frames.append(data)
    
    print("Recording finished.")
    
    stream.stop_stream()
    stream.close()
    p.terminate()
    
    wav_filename = "temp_audio.wav"
    with wave.open(wav_filename, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
        wf.setframerate(rate)
        wf.writeframes(b''.join(frames))
    
    print(f"Saved recording as {wav_filename}")
    
    return wav_filename

def convert_to_mp3(wav_filename, mp3_filename):
    audio = AudioSegment.from_wav(wav_filename)
    audio.export(mp3_filename, format="mp3")
    print(f"Saved MP3 as {mp3_filename}")
    

def transcribe_audio(filename):
    client = speech.SpeechClient()
    
    with io.open(filename, "rb") as audio_file:
        content = audio_file.read()
    
    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=44100,
        language_code="en-US"
    )
    
    response = client.recognize(config=config, audio=audio)
    
    for result in response.results:
        print("Transcript:", result.alternatives[0].transcript)
        return("You said, " + result.alternatives[0].transcript)
