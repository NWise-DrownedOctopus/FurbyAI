import socket
import threading
import time
import signal
import sys
import io
import unicodedata
import furby_utils as utils
from pydub import AudioSegment
from pydub.playback import play

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace', line_buffering=True)
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace', line_buffering=True)

# Global shutdown flag
running = True

def shutdown_signal_handler(signal_received, frame):
    global running
    print("\n[Shutdown] Signal received. Exiting gracefully...")
    running = False

# Register signal handlers
signal.signal(signal.SIGINT, shutdown_signal_handler)   # Ctrl+C
signal.signal(signal.SIGTERM, shutdown_signal_handler)  # kill command

def handle_connection(conn, addr):
    global running
    print(f"[Connection] Established with {addr}")
    conn.settimeout(90)

    while running:
        try:
            # Step 1: Prompt user for voice input
            wav_file = utils.record_audio("recorded_audio.wav", duration=5)
            utils.convert_to_mp3(wav_file, "recorded_audio.mp3")
            user_message = utils.transcribe_audio(wav_file)
            
            response = user_message

            # Step 2: Send transcribed message back to brain
            print(f"[User] → {user_message}")
            safe_response = sanitize(response)
            conn.sendall(user_message.encode('utf-8')) 
            
            # Step 3: Receive message from brain (Ollama response)
            data = conn.recv(1024).decode('utf-8')
            if not data:
                print("[Connection] Client disconnected.")
                break

            print(f"[Brain] → {data}")

            # Step 4: Play audio + run motor
            utils.synth_speech(data)
            audio = AudioSegment.from_mp3("output.mp3")
            duration_seconds = len(audio) / 1000

            audio_thread = threading.Thread(target=play, args=(audio,))
            motor_thread = threading.Thread(
                target=utils.runMotorTimed,
                args=(duration_seconds, 0)
            )

            audio_thread.start()
            motor_thread.start()
            audio_thread.join()
            motor_thread.join()

        except socket.timeout:
            print("[Timeout] No data received in 20 seconds.")
            break
        except Exception as e:
            print(f"[Error] Unexpected error in connection loop: {e}")
            break

    try:
        conn.close()
        print(f"[Connection] Closed with {addr}")
    except Exception as e:
        print(f"[Error] Closing connection: {e}")

def furbyConversation():
    global running
    HOST = '0.0.0.0'
    PORT = 65432

    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((HOST, PORT))
        server.listen()
        server.settimeout(5)

        print(f"[Server] Listening on {HOST}:{PORT}...")

        while running:
            try:
                conn, addr = server.accept()
                print(f"We are calling handle_connection()")
                handle_connection(conn, addr)
            except socket.timeout:
                continue
            except Exception as e:
                print(f"[Server Error] Accept failed: {e}")
                time.sleep(2)

    except Exception as e:
        print(f"[Startup Error] Could not start server: {e}")
    finally:
        try:
            server.close()
            print("[Server] Shutdown complete.")
        except:
            pass
            
def sanitize(text):
    return unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")

# Entry point
if __name__ == "__main__":
    furbyConversation()
