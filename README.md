# 🧠 FurbyAI – A Smart Assistant with Plastic Ears

### Author: Nicholas Wise  

---

![Furby Front View](https://github.com/user-attachments/assets/040fdc10-15df-4a84-9111-e49f46fd94e7)

Furby AI is a custom-built smart assistant housed inside a retro Furby animatronic. This project combines hardware hacking and AI to give new life to a nostalgic toy—transforming it into a fully interactive voice assistant. From modifying the electronics to writing all the software from scratch, every aspect of the project was personally built and engineered, with guidance from the UMKC Robotics team.

---

## 🛠️ Tech Breakdown

### 🧸 Furby "Body" – The Physical Puppet
Powered by a **Raspberry Pi 4**, the Furby's animatronic parts have been reanimated to receive input and deliver audio responses.

- Raspberry Pi 4
- Modified Furby animatronic (motors, power source)
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
