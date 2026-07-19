# Gesture Controller 🤟

An intelligent, webcam-based macro controller that uses local AI to translate hand gestures into physical Windows operating system commands. 

This project bypasses traditional input devices, allowing you to launch applications, execute keyboard shortcuts, and manage your workspace entirely hands-free. It features a custom background voice engine and a Smart Close system powered by a LIFO memory stack.

## ✨ Key Features

* **Real-Time Hand Tracking:** Utilizes Google's MediaPipe and OpenCV to map 21 3D landmarks onto the user's hand at 30+ FPS.
* **Smart App Management (LIFO Memory):** The system remembers the exact order in which you opened applications. Triggering the "Open Palm" gesture automatically decides whether to use `Alt + F4` (for desktop apps) or `Ctrl + W` (for browser tabs) based on the top of the memory stack.
* **Asynchronous Voice Engine:** Integrated `pyttsx3` with Python's `threading` module to provide real-time audio feedback without interrupting or freezing the active camera feed.
* **State Machine & Time Locks:** Built-in global cooldowns (2.0s) and gesture hold-timers (1.5s) to prevent accidental executions and spam-triggering.
* **Customizable Triggers:** Easily map distinct geometric finger patterns (e.g., Pinky Up, Victory, I Love You) to custom OS commands via `os.system` and `pyautogui`.

## 🛠️ Tech Stack

* **Language:** Python 3.x
* **Computer Vision:** OpenCV (`cv2`), MediaPipe
* **OS Automation:** PyAutoGUI, `os`
* **Audio/Feedback:** `pyttsx3`, `winsound`, `threading`

## 🚀 Installation & Setup

**1. Clone the repository**
```bash
git clone [https://github.com/YOUR-USERNAME/gesture-controller.git](https://github.com/thejesh-kumar-r/gesture-controller.git)
cd gesture-controller
