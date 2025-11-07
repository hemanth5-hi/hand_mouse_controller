# 🖐️ Hand Mouse Controller (AI-Powered Gesture Control)
🎯 Control your computer cursor using just your hand movements — no hardware required!

This project turns your webcam into an AI-based virtual mouse, letting you move, click, and drag using simple hand gestures powered by OpenCV and MediaPipe.

🚀 Features

✅ Real-time hand tracking using MediaPipe
✅ Mouse control with finger gestures (move, click, drag, scroll)
✅ Adjustable hand sensitivity via GUI
✅ Simple Tkinter interface to start, stop, or exit
✅ Failsafe protection and smooth cursor motion
✅ Works entirely offline — no external devices or cloud APIs

🧠 Tech Stack
Component	Library / Tool
Hand Tracking	MediaPipe

Computer Vision	OpenCV

Mouse Control	PyAutoGUI

GUI	Tkinter
Numerical Operations	NumPy
🧩 Project Structure
HandMouseController/
│
├── hand_mouse_gui.py        # Main project file
├── requirements.txt         # All dependencies
└── README.md                # Documentation (this file)

⚙️ Installation & Setup
1️⃣ Clone the repository
git clone https://github.com/<your-username>/HandMouseController.git
cd HandMouseController

2️⃣ Create a virtual environment (recommended)
python -m venv venv
venv\Scripts\activate   # On Windows
source venv/bin/activate  # On macOS / Linux

3️⃣ Install dependencies
pip install -r requirements.txt

4️⃣ Run the program
python hand_mouse_gui.py

🧾 requirements.txt
opencv-python==4.10.0.84
mediapipe==0.10.21
pyautogui==0.9.54
numpy==1.26.4
pillow==10.4.0

🎮 How to Use
Gesture	Action
🖐️ Move your hand	Move cursor
🤏 Thumb + Index close	Left Click
✌️ Index + Middle close	Right Click
🖐️ Hold pinch	Drag & Drop
✊ Closed fist	Scroll
🖱️ Sensitivity slider	Adjust movement smoothness
🪄 GUI Controls
Button	Function
▶️ Start Controller	Begin camera + gesture tracking
⏹️ Stop Controller	Stop camera safely
❌ Exit	Quit application
🎚️ Sensitivity Slider	Change hand tracking speed
🧠 How It Works

Captures video using your webcam via OpenCV

Detects hand landmarks using MediaPipe Hands model

Maps finger tip coordinates → screen coordinates

Uses PyAutoGUI to move the mouse & perform click actions

Smoothens movement for better stability

🧰 Troubleshooting
