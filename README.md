# 🎹 Virtual Piano Using Hand Gestures

This project is a **Virtual Piano** that allows users to play piano notes using hand gestures detected via a webcam. It leverages **Mediapipe** for hand tracking and **PyGame** for audio playback. The system detects which fingers are raised and plays corresponding piano sounds.

---

## 📖 Features

- **Real-time hand tracking**: Uses Mediapipe to detect hand landmarks.
- **Finger-based sound mapping**: Each finger is mapped to a unique piano note.
- **Multi-hand support**: Detects gestures from both left and right hands.
- **Asynchronous sound playback**: Ensures smooth and responsive sound output.
- **Full-screen display**: Provides an immersive piano-playing experience.

---

## 🛠️ Setup Instructions

### 1. Prerequisites
Ensure you have Python 3.8+ installed on your system.

### 2. Install Required Libraries
Run the following command to install the dependencies:

```bash
pip install opencv-python mediapipe pygame

```
### 3. Configure Sound Files
Store your .wav sound files in a directory (e.g., E:\piano\wav).
Update the finger_sounds dictionary in the script to match your file paths.

### 4. Run the Program
Use the following command to start the Virtual Piano:

```bash
python virtual_piano.py

## 🛠️ Technologies Used

- **Language/Framework**: Python
- **Libraries**: 
  - Pygame (for audio playback)
  - Mediapipe (for hand tracking)
  - OpenCV (for computer vision and webcam feed)
- **Tools**:
  - Visual Studio Code (for development)
  - Git (for version control)
 
## 🌟 Future Enhancements

- Add multiple levels of increasing difficulty.
- Implement power-ups and bonuses.
- Add a leaderboard for players to compete globally.
- Include sound effects for different hand gestures.
- Optimize hand detection for faster response time.

---

## 🧑‍💻 Contributing

Contributions are welcome! Feel free to:

1. Fork the repository.
2. Make your changes.
3. Submit a pull request.

---

## 🖍️ License

This project is licensed under the **MIT License**.

---

## 📩 Contact

For questions or feedback, reach out via:  
**Email**: batrapulkit1103@gmail.com




