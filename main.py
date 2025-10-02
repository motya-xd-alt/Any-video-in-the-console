import cv2
import os
import time
import shutil

# A set of characters from "empty" to "filled"
ASCII_CHARS = " .:-=+*#%@"

def frame_to_ascii(frame, new_width=100):
    # Converting to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # We determine the new size for the console width
    height, width = gray.shape
    aspect_ratio = height / width
    new_height = int(aspect_ratio * new_width * 0.55)  # 0.55 to maintain proportions

    resized = cv2.resize(gray, (new_width, new_height))

    # We translate each pixel into a symbol
    ascii_frame = ""
    for row in resized:
        for pixel in row:
            ascii_frame += ASCII_CHARS[pixel * len(ASCII_CHARS) // 256]
        ascii_frame += "\n"

    return ascii_frame

def play_video_ascii(video_path):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Не удалось открыть видео.")
        return

    # Determine the FPS for playback synchronization
    fps = cap.get(cv2.CAP_PROP_FPS)
    delay = 1 / fps if fps > 0 else 0.03

    # Find out the size of the console
    term_size = shutil.get_terminal_size((100, 40))
    new_width = min(term_size.columns, 120)  # Let's limit the width

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            ascii_frame = frame_to_ascii(frame, new_width=new_width)

            # Clearing the screen (Windows/Linux)
            os.system("cls" if os.name == "nt" else "clear")

            print(ascii_frame)

            time.sleep(delay)

    except KeyboardInterrupt:
        print("\nStopped by user.")
    finally:
        cap.release()

if __name__ == "__main__":
    play_video_ascii("video.mp4")  # Specify the path to your video
