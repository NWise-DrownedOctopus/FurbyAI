import socket
import threading
import time
import signal
import furby_utils as utils
from pydub import AudioSegment
from pydub.playback import play
from pydub import AudioSegment

# User Shutdown Flag
running = True

def shutdown_signal_handler(signal, frame):
	global running
	print("Shutdown initiated")
	running = False
	
# Here we register the signal handler
signal.signal(signal.SIGINT, shutdown_signal_handler)  # Ctrl+C
signal.signal(signal.SIGTERM, shutdown_signal_handler)  # kill command

# This Function will wait for a thought to come from the brain server
def furbyConversation():
	global running
	# Listining on all network interfaces	
	HOST = '0.0.0.0'
	PORT = 65432
	
	while running:
		server = None
		conn = None
		try:
			# Here we establish a basic TCP network, and then listen for a 
			# reponse from the Furby Brain
			server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			server.bind((HOST, PORT))
			server.listen()			
			print(f"Server listening on {HOST}:{PORT}...")
	
			# Sit here at wait for connection to be established
			conn, addr = server.accept()
			print(f"Connection established with {addr}")
			
			conn.settimeout(20)
			while running:
				try:
					data = conn.recv(1024).decode()
					if not data:
						print("Client disconnected.")
						break
					print(f"Received: {data}")
					
					wav_file = utils.record_audio("recorded_audio.mp3", duration=5)
					utils.convert_to_mp3(wav_file, "recorded_audio.mp3")
					userMessage = utils.transcribe_audio(wav_file)
					
					# Send response back to client
					response = userMessage
					conn.sendall(response.encode())		
					
					# Generate and play response					
					utils.synth_speech(data)
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
					
					conn.close()
					server.close()
					
				except socket.timeout:
					print("No Data recived for 20 seconds")
					break
			
		except Exception as e:
			print(f"Connection error: {e}")
		
		finally:
			if conn:
				conn.close()
			if server:
				server.close()
				
		if running:
			print("Restarting connection connection logic in 5 sec...")
			time.sleep(5)
	
	print("Furby has shutdown")
