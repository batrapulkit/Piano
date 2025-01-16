import cv2
import mediapipe as mp
import pygame
import threading
import streamlit as st
import numpy as np
from PIL import Image

# Initialize PyGame for sound
pygame.mixer.init()

# Mapping sounds to each finger (using .wav files in the 'wav' folder)
finger_sounds = {
    "thumb_left": pygame.mixer.Sound(r"./wav/A4.wav"),
    "index_left": pygame.mixer.Sound(r"./wav/B4.wav"),
    "middle_left": pygame.mixer.Sound(r"./wav/C4.wav"),
    "ring_left": pygame.mixer.Sound(r"./wav/D4.wav"),
    "pinky_left": pygame.mixer.Sound(r"./wav/E4.wav"),
    "thumb_right": pygame.mixer.Sound(r"./wav/F4.wav"),
    "index_right": pygame.mixer.Sound(r"./wav/G4.wav"),
    "middle_right": pygame.mixer.Sound(r"./wav/D5.wav"),
    "ring_right": pygame.mixer.Sound(r"./wav/E5.wav"),
    "pinky_right": pygame.mixer.Sound(r"./wav/C5.wav"),
}

# Initialize Mediapipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# To track which fingers have already played their sounds
played_fingers = set()

# Function to play sound asynchronously
def play_sound(sound):
    sound.play()

# Streamlit app title
st.title("Virtual Piano Hand Tracker")

# Start the webcam feed using OpenCV
cap = cv2.VideoCapture(0)

# Define a placeholder for the webcam feed
frame_placeholder = st.empty()

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

    # Convert the frame to an image compatible with Streamlit and update the placeholder
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img_pil = Image.fromarray(frame_rgb)
    frame_placeholder.image(img_pil, channels="RGB", use_column_width=True)

# Release the webcam when the app is closed
cap.release()
pygame.quit()
