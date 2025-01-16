import cv2
import mediapipe as mp
import pygame
import threading

# Initialize Mediapipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Initialize PyGame for sound
pygame.init()

# Mapping sounds to each finger (using .wav files from E:\piano\wav)
finger_sounds = {
    "thumb_left": pygame.mixer.Sound(r"E:\piano\wav\A4.wav"),
    "index_left": pygame.mixer.Sound(r"E:\piano\wav\B4.wav"),
    "middle_left": pygame.mixer.Sound(r"E:\piano\wav\C4.wav"),
    "ring_left": pygame.mixer.Sound(r"E:\piano\wav\D4.wav"),
    "pinky_left": pygame.mixer.Sound(r"E:\piano\wav\E4.wav"),
    "thumb_right": pygame.mixer.Sound(r"E:\piano\wav\F4.wav"),
    "index_right": pygame.mixer.Sound(r"E:\piano\wav\G4.wav"),
    "middle_right": pygame.mixer.Sound(r"E:\piano\wav\D5.wav"),
    "ring_right": pygame.mixer.Sound(r"E:\piano\wav\E5.wav"),
    "pinky_right": pygame.mixer.Sound(r"E:\piano\wav\C5.wav"),
}

# Webcam feed
cap = cv2.VideoCapture(0)

# Full-screen display
cv2.namedWindow("Virtual Piano", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("Virtual Piano", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

# To track which fingers have already played their sounds
played_fingers = set()

# Function to play sound asynchronously
def play_sound(sound):
    sound.play()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Flip the frame horizontally
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    # Process hand landmarks
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Get fingertip and MCP (knuckle) coordinates for each finger
            landmarks = hand_landmarks.landmark
            thumb_tip = landmarks[mp_hands.HandLandmark.THUMB_TIP].y
            index_tip = landmarks[mp_hands.HandLandmark.INDEX_FINGER_TIP].y
            middle_tip = landmarks[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y
            ring_tip = landmarks[mp_hands.HandLandmark.RING_FINGER_TIP].y
            pinky_tip = landmarks[mp_hands.HandLandmark.PINKY_TIP].y

            thumb_mcp = landmarks[mp_hands.HandLandmark.THUMB_CMC].y
            index_mcp = landmarks[mp_hands.HandLandmark.INDEX_FINGER_MCP].y
            middle_mcp = landmarks[mp_hands.HandLandmark.MIDDLE_FINGER_MCP].y
            ring_mcp = landmarks[mp_hands.HandLandmark.RING_FINGER_MCP].y
            pinky_mcp = landmarks[mp_hands.HandLandmark.PINKY_MCP].y

            # Determine the hand (left or right) based on wrist position
            wrist_x = landmarks[mp_hands.HandLandmark.WRIST].x
            hand_prefix = "left" if wrist_x < 0.5 else "right"

            # Check if the thumb is raised (thumb tip above thumb MCP)
            if thumb_tip < thumb_mcp and f"thumb_{hand_prefix}" not in played_fingers:
                threading.Thread(target=play_sound, args=(finger_sounds[f"thumb_{hand_prefix}"],)).start()
                played_fingers.add(f"thumb_{hand_prefix}")
            elif thumb_tip >= thumb_mcp:
                played_fingers.discard(f"thumb_{hand_prefix}")

            # Check for other fingers (index, middle, ring, pinky)
            if index_tip < index_mcp and f"index_{hand_prefix}" not in played_fingers:
                threading.Thread(target=play_sound, args=(finger_sounds[f"index_{hand_prefix}"],)).start()
                played_fingers.add(f"index_{hand_prefix}")
            elif index_tip >= index_mcp:
                played_fingers.discard(f"index_{hand_prefix}")

            if middle_tip < middle_mcp and f"middle_{hand_prefix}" not in played_fingers:
                threading.Thread(target=play_sound, args=(finger_sounds[f"middle_{hand_prefix}"],)).start()
                played_fingers.add(f"middle_{hand_prefix}")
            elif middle_tip >= middle_mcp:
                played_fingers.discard(f"middle_{hand_prefix}")

            if ring_tip < ring_mcp and f"ring_{hand_prefix}" not in played_fingers:
                threading.Thread(target=play_sound, args=(finger_sounds[f"ring_{hand_prefix}"],)).start()
                played_fingers.add(f"ring_{hand_prefix}")
            elif ring_tip >= ring_mcp:
                played_fingers.discard(f"ring_{hand_prefix}")

            if pinky_tip < pinky_mcp and f"pinky_{hand_prefix}" not in played_fingers:
                threading.Thread(target=play_sound, args=(finger_sounds[f"pinky_{hand_prefix}"],)).start()
                played_fingers.add(f"pinky_{hand_prefix}")
            elif pinky_tip >= pinky_mcp:
                played_fingers.discard(f"pinky_{hand_prefix}")

    # Display the frame
    cv2.imshow("Virtual Piano", frame)

    # Quit on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
pygame.quit()
