import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import threading
import time
import tkinter as tk
from tkinter import messagebox

# Disable PyAutoGUI failsafe
pyautogui.FAILSAFE = False

# Initialize mediapipe
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Global control variables
running = False
drag_mode = False
last_click_time = 0
smoothening = 5     # Default sensitivity
prev_x, prev_y = 0, 0

# Screen dimensions
screen_w, screen_h = pyautogui.size()

def euclidean_distance(x1, y1, x2, y2):
    return np.hypot(x2 - x1, y2 - y1)

def hand_mouse_control():
    global running, drag_mode, last_click_time, prev_x, prev_y, smoothening

    hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
    cap = cv2.VideoCapture(0)

    while running:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                h, w, _ = frame.shape
                lm = hand_landmarks.landmark

                index_finger = (int(lm[8].x * w), int(lm[8].y * h))
                thumb = (int(lm[4].x * w), int(lm[4].y * h))
                middle_finger = (int(lm[12].x * w), int(lm[12].y * h))

                # Convert to screen coordinates
                x3 = np.interp(index_finger[0], (100, w - 100), (0, screen_w))
                y3 = np.interp(index_finger[1], (100, h - 100), (0, screen_h))

                curr_x = prev_x + (x3 - prev_x) / smoothening
                curr_y = prev_y + (y3 - prev_y) / smoothening

                safe_x = np.clip(curr_x, 10, screen_w - 10)
                safe_y = np.clip(curr_y, 10, screen_h - 10)
                pyautogui.moveTo(safe_x, safe_y)
                prev_x, prev_y = curr_x, curr_y

                # Calculate distances
                dist_thumb_index = euclidean_distance(*index_finger, *thumb)
                dist_index_middle = euclidean_distance(*index_finger, *middle_finger)

                # Left Click
                if dist_thumb_index < 30:
                    if time.time() - last_click_time > 0.4:
                        pyautogui.click()
                        last_click_time = time.time()
                        cv2.putText(frame, "Left Click", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

                # Right Click
                elif dist_index_middle < 35:
                    if time.time() - last_click_time > 0.6:
                        pyautogui.click(button='right')
                        last_click_time = time.time()
                        cv2.putText(frame, "Right Click", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

                # Drag & Drop
                if dist_thumb_index < 35:
                    if not drag_mode:
                        pyautogui.mouseDown()
                        drag_mode = True
                        cv2.putText(frame, "Dragging...", (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
                else:
                    if drag_mode:
                        pyautogui.mouseUp()
                        drag_mode = False

                # Scroll (closed fist)
                if dist_thumb_index < 45 and dist_index_middle < 45:
                    pyautogui.scroll(-20)
                    cv2.putText(frame, "Scrolling...", (10, 130), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        cv2.imshow("🖐️ Hand Mouse Controller", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            running = False
            break

    cap.release()
    cv2.destroyAllWindows()

def start_controller():
    global running
    if not running:
        running = True
        threading.Thread(target=hand_mouse_control, daemon=True).start()
        messagebox.showinfo("Started", "Hand Mouse Controller is now running!")
    else:
        messagebox.showinfo("Info", "Already running!")

def stop_controller():
    global running
    running = False
    messagebox.showinfo("Stopped", "Hand Mouse Controller stopped!")

def exit_app():
    global running
    running = False
    root.destroy()

def update_sensitivity(value):
    """Update smoothening based on slider (lower value = faster mouse)."""
    global smoothening
    smoothening = float(value)
    sensitivity_label.config(text=f"Sensitivity: {smoothening:.1f}")

# -------------------- GUI --------------------
root = tk.Tk()
root.title("🖐️ Hand Mouse Controller")
root.geometry("380x360")
root.configure(bg="#1e1e1e")

tk.Label(root, text="🖐️ Hand Mouse Controller", font=("Helvetica", 16, "bold"), fg="white", bg="#1e1e1e").pack(pady=15)

tk.Button(root, text="▶️ Start Controller", font=("Helvetica", 12, "bold"), bg="#2ecc71", fg="white", width=20, command=start_controller).pack(pady=8)
tk.Button(root, text="⏹️ Stop Controller", font=("Helvetica", 12, "bold"), bg="#e67e22", fg="white", width=20, command=stop_controller).pack(pady=8)
tk.Button(root, text="❌ Exit", font=("Helvetica", 12, "bold"), bg="#e74c3c", fg="white", width=20, command=exit_app).pack(pady=8)

# Sensitivity slider
tk.Label(root, text="Adjust Hand Sensitivity", font=("Helvetica", 12, "bold"), fg="white", bg="#1e1e1e").pack(pady=8)
sensitivity_slider = tk.Scale(root, from_=2, to=10, resolution=0.5, orient="horizontal",
                              length=250, command=update_sensitivity, bg="#1e1e1e", fg="white")
sensitivity_slider.set(smoothening)
sensitivity_slider.pack()

sensitivity_label = tk.Label(root, text=f"Sensitivity: {smoothening}", fg="lightgray", bg="#1e1e1e", font=("Helvetica", 10))
sensitivity_label.pack()

tk.Label(root, text="Gestures:\n🖐️ Move hand = Move cursor\n🤏 Thumb+Index = Left Click\n✌️ Thumb+Middle = Right Click\n✋ Hold pinch = Drag\n✊ Fist = Scroll",
         fg="lightgray", bg="#1e1e1e", font=("Helvetica", 9)).pack(pady=10)

root.mainloop()
