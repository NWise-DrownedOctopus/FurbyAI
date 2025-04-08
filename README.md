This is already a solid start! You've got a clear structure, great photos, and a good breakdown of the tech. Below is a more polished, engaging version of your README—keeps all the core info but gives it a little more voice and flow, plus improved formatting and some small fixes (like “Raspberry Pi” spelling 😄):

---

# 🧠 FurbyAI – A Smart Assistant with Plastic Ears

### Author: Nicholas Wise  

---

![Furby Front View](https://github.com/user-attachments/assets/040fdc10-15df-4a84-9111-e49f46fd94e7)

**FurbyAI** is what happens when you combine a retro toy, modern AI, and some good old-fashioned hardware hacking. This project transforms a classic Furby animatronic into a fully interactive smart assistant—complete with real-time voice recognition, AI-generated responses, and blinking eyelids that watch your every move.

All hardware modifications and software development were done by me, with guidance from the UMKC Robotics team.

---

## 🛠️ Tech Breakdown

### 🧸 Furby "Body" – The Physical Puppet
Powered by a **Raspberry Pi 4**, the Furby's animatronic parts have been reanimated to receive input and deliver audio responses.

- Raspberry Pi 4
- Modified Furby animatronic (motors, speaker, mic)
- Audio input/output
- Google Cloud:
  - **Speech-to-Text** for transcription
  - **Text-to-Speech** for AI voice output

### 🧠 Furby "Brain" – The AI Engine
The Raspberry Pi connects to a more powerful desktop machine that handles natural language understanding and response generation.

- Desktop Linux (Ubuntu)
- **DeepSeek-R1 (1.5b)** running locally
- **Ollama** for model serving

### 🔗 Furby "Spine" – The Nervous System
The communication between the Furby's body and its AI brain is handled via lightweight socket connections written in Python.

- Python `socket` library for device-to-device messaging

---

## 🔊 Wake Word Support (In Progress)
To avoid sending continuous audio to Google services, FurbyAI will soon include **offline wake word detection** using [Porcupine by Picovoice](https://picovoice.ai/platform/porcupine/). Once Furby hears “Hey Furby,” it will begin listening for prompts.

---

## 📸 Project Photos
![Furby Side View](https://github.com/user-attachments/assets/75d70d56-7885-410f-8e29-a12befb23476)

---

If you have questions, want to contribute ideas, or just want to say hi to Furby, feel free to open an issue or drop a message!

---

Let me know if you want to include a demo video section, a to-do list, or some setup instructions later on!
