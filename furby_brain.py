import socket
import furby_brain_utils as utils
HOST = '10.10.3.120'
PORT = 65432

# Here we attept to create a TCP connection with the main furby body
try:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.settimeout(90)
    client.connect((HOST, PORT))
    print(f"Connected to server. Type 'exit' to disconnect.")
except socket.error as e:
    print(f"failed to connect to server: {e}")
    exit(1)

while True:
        try:
            prompt = client.recv(1024).decode('utf-8')
            if not prompt:
                print("Server disconnected.")
                break
            print(f"Server: {prompt}")
            response = utils.ollama_chat(prompt)
            print("Ollama:", response)

            # send message to server
            message = utils.clean_response(response)
            safe_response = utils.sanitize(response)
            client.sendall(message.encode('utf-8'))

            # exit if user says exit
            if message.lower() == "exit":
                break    

        except socket.timeout:
            print("Socket timeout: No message recived.")
        except socket.error as e:
            print(f"Socket error: {e}")
            break
        except Exception as e:
            print(f"Unexpected error during processing: {e}")
            break
