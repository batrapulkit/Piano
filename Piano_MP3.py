import cv2
import mediapipe as mp
import pygame

# Initialize Mediapipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Initialize PyGame for sound
pygame.init()

# Mapping sounds to each finger
finger_sounds = {
    "thumb_left": pygame.mixer.Sound("sounds/A4.mp3"),
    "index_left": pygame.mixer.Sound("sounds/B4.mp3"),
    "middle_left": pygame.mixer.Sound("sounds/C4.mp3"),
    "ring_left": pygame.mixer.Sound("sounds/D4.mp3"),
    "pinky_left": pygame.mixer.Sound("sounds/E4.mp3"),
    "thumb_right": pygame.mixer.Sound("sounds/F4.mp3"),
    "index_right": pygame.mixer.Sound("sounds/G4.mp3"),
    "middle_right": pygame.mixer.Sound("sounds/D5.mp3"),
    "ring_right": pygame.mixer.Sound("sounds/E5.mp3"),
    "pinky_right": pygame.mixer.Sound("sounds/C5.mp3"),
}

# Webcam feed
cap = cv2.VideoCapture(0)

# Full-screen display
cv2.namedWindow("Virtual Piano", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("Virtual Piano", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

# To track which fingers have already played their sounds
played_fingers = set()

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

            # Determine the hand (left or right) based on landmark positions
            if landmarks[mp_hands.HandLandmark.WRIST].x < frame.shape[1] // 2:
                hand_prefix = "left"
            else:
                hand_prefix = "right"

            # Check if the fingertip is above the corresponding MCP (i.e., finger is raised)
            if thumb_tip < thumb_mcp and f"thumb_{hand_prefix}" not in played_fingers:
                finger_sounds[f"thumb_{hand_prefix}"].play()
                played_fingers.add(f"thumb_{hand_prefix}")
            elif thumb_tip >= thumb_mcp:
                played_fingers.discard(f"thumb_{hand_prefix}")

            if index_tip < index_mcp and f"index_{hand_prefix}" not in played_fingers:
                finger_sounds[f"index_{hand_prefix}"].play()
                played_fingers.add(f"index_{hand_prefix}")
            elif index_tip >= index_mcp:
                played_fingers.discard(f"index_{hand_prefix}")

            if middle_tip < middle_mcp and f"middle_{hand_prefix}" not in played_fingers:
                finger_sounds[f"middle_{hand_prefix}"].play()
                played_fingers.add(f"middle_{hand_prefix}")
            elif middle_tip >= middle_mcp:
                played_fingers.discard(f"middle_{hand_prefix}")

            if ring_tip < ring_mcp and f"ring_{hand_prefix}" not in played_fingers:
                finger_sounds[f"ring_{hand_prefix}"].play()
                played_fingers.add(f"ring_{hand_prefix}")
            elif ring_tip >= ring_mcp:
                played_fingers.discard(f"ring_{hand_prefix}")

            if pinky_tip < pinky_mcp and f"pinky_{hand_prefix}" not in played_fingers:
                finger_sounds[f"pinky_{hand_prefix}"].play()
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
