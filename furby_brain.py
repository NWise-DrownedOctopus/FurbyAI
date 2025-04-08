import socket
import furby_brain_utils as utils
HOST = '10.10.3.120'
PORT = 65432

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

print("Connected to the server. Type 'exit' to disconnect.")

while True:
    prompt = client.recv(1024).decode()
    if not prompt:
        print("Server disconnected.")
        break
    print(f"Server: {prompt}")

    # Example usage
    response = utils.ollama_chat(prompt)
    print("Ollama:", response)

    #send message to server
    message = utils.clean_response(response)
    client.sendall(message.encode())

    if message.lower() == "exit":
        break    

client.close()
