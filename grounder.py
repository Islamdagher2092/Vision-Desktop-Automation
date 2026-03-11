import cv2
import easyocr
import mss
import numpy as np
import os
from datetime import datetime

class IconGrounder:
    def __init__(self):
        print("Initializing Vision Grounding Model (EasyOCR)...")
        self.reader = easyocr.Reader(['en'], gpu=False)
        self.screenshots_dir = "annotated_screenshots"
        os.makedirs(self.screenshots_dir, exist_ok=True)

    def capture_screen(self) -> np.ndarray:
        with mss.mss() as sct:
            monitor = sct.monitors[1]
            screenshot = sct.grab(monitor)
            img = np.array(screenshot)
            img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
            return img

    def locate_icon_by_text(self, target_text: str = "Notepad") -> tuple[int, int] | None:
        image = self.capture_screen()
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        results = self.reader.readtext(gray)
        
        for (bbox, text, prob) in results:
            if target_text.lower() in text.lower():
                top_left = (int(bbox[0][0]), int(bbox[0][1]))
                bottom_right = (int(bbox[2][0]), int(bbox[2][1]))
                
                cv2.rectangle(image, top_left, bottom_right, (0, 0, 255), 3)
                cv2.putText(image, f"{text} ({prob:.2f})", (top_left[0], top_left[1] - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
                
                timestamp = datetime.now().strftime("%H%M%S")
                save_path = os.path.join(self.screenshots_dir, f"grounded_{timestamp}.png")
                cv2.imwrite(save_path, image)
                print(f"Annotated screenshot saved to: {save_path}")
                
                center_x = int((top_left[0] + bottom_right[0]) / 2)
                center_y = int((top_left[1] + bottom_right[1]) / 2)
                return (center_x, center_y)
                
        return None