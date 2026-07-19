import cv2
import mediapipe as mp
import pyautogui
import time
import os
import winsound
import pyttsx3
import threading

# --- 1. THE VOICE ENGINE ---
def speak(text):
    """Runs completely in the background so the camera doesn't freeze."""
    engine = pyttsx3.init()
    engine.setProperty('rate', 170) # Adjust speed here (default is usually 200)
    # Optional: Change voice from male to female
    # voices = engine.getProperty('voices')
    # engine.setProperty('voice', voices[1].id) 
    engine.say(text)
    engine.runAndWait()

# --- 2. INITIALIZE AI & CAMERA ---
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0) 

# --- 3. MEMORY & TIMER VARIABLES ---
last_action_time = 0
cooldown_seconds = 2.0  
app_history = []  # The LIFO memory stack for Smart Close

current_held_gesture = "Waiting..."
gesture_start_time = 0
required_hold_time = 0.9  

# Announce startup!
threading.Thread(target=speak, args=("System online. Waiting for commands.",)).start()
print("Master Macro System Initialized. Waiting for commands...")

# --- 4. THE MAIN VISION LOOP ---
while True:
    success, frame = cap.read()
    if not success:
        time.sleep(4)
        break

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    detected_gesture = "Waiting..."
    current_time = time.time()
    action_triggered = False

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
            landmarks = hand_landmarks.landmark
            thumb_tip, index_pip = landmarks[4], landmarks[6]
            wrist = landmarks[0]

            # Map the 4 main fingers (True = Up, False = Down)
            fingers_up = [
                landmarks[8].y < landmarks[6].y,   # Index
                landmarks[12].y < landmarks[10].y, # Middle
                landmarks[16].y < landmarks[14].y, # Ring
                landmarks[20].y < landmarks[18].y  # Pinky
            ]

            # --- STEP 1: DETECT THE GESTURE ---
            if fingers_up == [True, True, True, True]:
                detected_gesture = "Open Palm"
            elif fingers_up == [True, False, False, False]:
                detected_gesture = "Pointing Up"
            elif fingers_up == [True, True, False, False]:
                detected_gesture = "Victory"
            elif fingers_up == [False, False, False, True]: # NEW CUSTOM GESTURE
                detected_gesture = "Pinky Up"
            elif fingers_up == [True, False, False, True] and (thumb_tip.x < index_pip.x or thumb_tip.x > landmarks[18].x): 
                detected_gesture = "I Love You"
            elif fingers_up == [False, False, False, False]:
                if thumb_tip.y < index_pip.y: 
                    detected_gesture = "Thumbs Up"
                elif thumb_tip.y > wrist.y: 
                    detected_gesture = "Thumbs Down"
                else: 
                    detected_gesture = "Closed Fist"

    # --- STEP 2: THE HOLD TIMER LOGIC ---
    time_since_last_action = current_time - last_action_time
    is_cooling_down = time_since_last_action < cooldown_seconds

    if detected_gesture != "Waiting...":
        
        if detected_gesture == current_held_gesture:
            
            if is_cooling_down:
                cooldown_left = cooldown_seconds - time_since_last_action
                cv2.putText(frame, f"Cooldown: {cooldown_left:.1f}s", (10, 90), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2, cv2.LINE_AA)
                gesture_start_time = current_time 
                
            else:
                hold_duration = current_time - gesture_start_time
                cv2.putText(frame, f"Holding: {hold_duration:.1f}s / {required_hold_time}s", (10, 90), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2, cv2.LINE_AA)

                if hold_duration >= required_hold_time:
                    
                    last_app = app_history[-1] if len(app_history) > 0 else ""

                    # --- STEP 3: EXECUTE THE ACTIONS ---
                    
                    # 1. SMART CLOSE
                    if detected_gesture == "Open Palm":
                        if len(app_history) > 0:
                            app_to_close = app_history.pop() 
                            print(f"Action: Closing {app_to_close}")
                            threading.Thread(target=speak, args=(f"Closing {app_to_close}",)).start()
                            
                            if app_to_close in ["Outlook", "VS Code"]:
                                pyautogui.hotkey('alt', 'f4')
                            else:
                                pyautogui.hotkey('ctrl', 'w')
                        else:
                            print("Action: Closing Current Window (Fallback)")
                            pyautogui.hotkey('ctrl', 'w')
                        action_triggered = True

                    # 2. OUTLOOK
                    elif detected_gesture == "Pointing Up" and last_app != "Outlook":
                        print("Action: Opening Outlook App")
                        threading.Thread(target=speak, args=("Opening Outlook.",)).start()
                        pyautogui.press('win')         
                        time.sleep(0.5)                
                        pyautogui.write('Outlook')     
                        time.sleep(0.5)                
                        pyautogui.press('enter')       
                        app_history.append("Outlook") 
                        action_triggered = True

                    # 3. INSTAGRAM
                    elif detected_gesture == "Victory" and last_app != "Instagram":
                        print("Action: Opening Instagram")
                        threading.Thread(target=speak, args=("Opening Instagram.",)).start()
                        os.system("start msedge https://instagram.com")
                        app_history.append("Instagram")
                        action_triggered = True
                        
                    # 4. YOUTUBE (CUSTOM GESTURE)
                    elif detected_gesture == "Pinky Up" and last_app != "YouTube":
                        print("Action: Opening YouTube")
                        threading.Thread(target=speak, args=("Opening Youtube.",)).start()
                        os.system("start chrome https://youtube.com")
                        app_history.append("YouTube")
                        action_triggered = True

                    # 5. SHUTDOWN
                    elif detected_gesture == "I Love You":
                        print("Action: Shutting Down")
                        threading.Thread(target=speak, args=("Shutting down. Goodbye.",)).start()
                        time.sleep(1.5) # Wait briefly so the voice can finish before killing the script
                        cap.release()
                        cv2.destroyAllWindows()
                        exit() 

                    # 6. VS CODE
                    elif detected_gesture == "Thumbs Up" and last_app != "VS Code":
                        print("Action: Opening VS Code App")
                        threading.Thread(target=speak, args=("Launching Visual Studio Code.",)).start()
                        os.system("code")
                        app_history.append("VS Code")
                        action_triggered = True
                            
                    # 7. SPOTIFY
                    elif detected_gesture == "Thumbs Down" and last_app != "Spotify":
                        print("Action: Opening Spotify")
                        threading.Thread(target=speak, args=("Loading Spotify.",)).start()
                        os.system("start chrome https://open.spotify.com")
                        app_history.append("Spotify")
                        action_triggered = True
                            
                    # 8. GEMINI
                    elif detected_gesture == "Closed Fist" and last_app != "Gemini":
                        print("Action: Opening Gemini")
                        threading.Thread(target=speak, args=("Accessing Gemini.",)).start()
                        os.system("start chrome https://gemini.google.com")
                        app_history.append("Gemini")
                        action_triggered = True

                    # Trigger Backup Audio and Reset Timers
                    if action_triggered:
                        winsound.MessageBeep(winsound.MB_OK)
                        last_action_time = current_time
                        gesture_start_time = current_time 

        else:
            current_held_gesture = detected_gesture
            gesture_start_time = current_time
    else:
        current_held_gesture = "Waiting..."
        gesture_start_time = current_time

    # --- 5. UI DISPLAY ---
    cv2.putText(frame, f"Target: {current_held_gesture}", (10, 50), 
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
    
    cv2.imshow("Gesture Macro Controller", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()