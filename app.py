import mediapipe as mp
import threading
import streamlit as st
import numpy as np
from PIL import Image
import io

# Mock sound playing for cloud deployment (just prints the sound file)
def play_sound(sound):
    print("Sound played:", sound)

# Mapping sounds to each finger (using .wav files in the 'wav' folder)import mediapipe as mp
import threading
import streamlit as st
import numpy as np
from PIL import Image
import io

# Mock sound playing for cloud deployment (just prints the sound file)
def play_sound(sound):
    print("Sound played:", sound)

# Mapping sounds to each finger (using .wav files in the 'wav' folder)
finger_sounds = {
    "thumb_left": "./wav/A4.wav",
    "index_left": "./wav/B4.wav",
    "middle_left": "./wav/C4.wav",
    "ring_left": "./wav/D4.wav",
    "pinky_left": "./wav/E4.wav",
    "thumb_right": "./wav/F4.wav",
    "index_right": "./wav/G4.wav",
    "middle_right": "./wav/D5.wav",
    "ring_right": "./wav/E5.wav",
    "pinky_right": "./wav/C5.wav",
}

# Initialize Mediapipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# To track which fingers have already played their sounds
played_fingers = set()

# Streamlit app title
st.title("Virtual Piano Hand Tracker")

# Use Streamlit's built-in camera input
camera_input = st.camera_input("Capture your hand gestures")

if camera_input is not None:
    # Convert the camera input (image) into a PIL format (which is compatible with Mediapipe)
    image = Image.open(camera_input)

    # Convert PIL image to numpy array (required by MediaPipe)
    img_array = np.array(image)

    # Convert to RGB (required by MediaPipe, since PIL opens in RGBA by default)
    rgb_image = img_array[..., :3]

    # Process the image using MediaPipe for hand landmarks
    results = hands.process(rgb_image)

    # If hand landmarks are found, process them
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(rgb_image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

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

    # Convert processed image back to PIL format for Streamlit display
    img_pil = Image.fromarray(rgb_image)

    # Display the image in Streamlit
    st.image(img_pil, channels="RGB", use_column_width=True)

    "thumb_left": "./wav/A4.wav",
    "index_left": "./wav/B4.wav",
    "middle_left": "./wav/C4.wav",
    "ring_left": "./wav/D4.wav",
    "pinky_left": "./wav/E4.wav",
    "thumb_right": "./wav/F4.wav",
    "index_right": "./wav/G4.wav",
    "middle_right": "./wav/D5.wav",
    "ring_right": "./wav/E5.wav",
    "pinky_right": "./wav/C5.wav",
}

# Initialize Mediapipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# To track which fingers have already played their sounds
played_fingers = set()

# Streamlit app title
st.title("Virtual Piano Hand Tracker")

# Use Streamlit's built-in camera input
camera_input = st.camera_input("Capture your hand gestures")

if camera_input is not None:
    # Convert the camera input (image) into a PIL format (which is compatible with Mediapipe)
    image = Image.open(camera_input)

    # Convert PIL image to numpy array (required by MediaPipe)
    img_array = np.array(image)

    # Convert to RGB (required by MediaPipe, since PIL opens in RGBA by default)
    rgb_image = cv2.cvtColor(img_array, cv2.COLOR_RGBA2RGB)

    # Process the image using MediaPipe for hand landmarks
    results = hands.process(rgb_image)

    # If hand landmarks are found, process them
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(rgb_image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

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

    # Convert processed image back to PIL format for Streamlit display
    img_pil = Image.fromarray(rgb_image)

    # Display the image in Streamlit
    st.image(img_pil, channels="RGB", use_column_width=True)
