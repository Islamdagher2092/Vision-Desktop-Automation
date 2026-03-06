# Vision-Based Desktop Automation 🤖👁️

A robust, Proof-of-Concept (PoC) Robotic Process Automation (RPA) tool that utilizes Computer Vision and OCR to dynamically locate UI elements and automate data entry tasks.

## 🚀 Overview
Unlike traditional automation scripts that rely on brittle, hard-coded screen coordinates or simple template matching, this project uses **Semantic Vision Grounding**. By leveraging `EasyOCR` and `OpenCV`, the agent "reads" the screen to find the target application (Notepad), making the script resolution-independent and highly resilient to UI changes.

## ✨ Key Features
* **Dynamic Vision Grounding:** Locates the target application anywhere on the screen using text recognition.
* **Robust Error Handling & Retry Logic:** Automatically retries UI interactions if the target window does not activate in time.
* **Graceful Degradation:** Features a fallback mechanism that generates local dummy data if the external API becomes unreachable.
* **Clean State Execution:** Handles OS-level interruptions (e.g., existing file overwrite prompts, lingering Notepad tabs in Windows 11) using forced process termination and automated UI cleanups.
* **High-Speed Data Entry:** Utilizes clipboard operations (`pyperclip`) to bypass the unreliability of standard keystroke simulation during large text entries.

## 🛠️ Tech Stack
* **Language:** Python 3
* **Package Manager:** `uv` (for fast, reproducible environments)
* **Vision & OCR:** `EasyOCR`, `OpenCV` (`cv2`), `mss`
* **Automation:** `PyAutoGUI`, `PyGetWindow`, `pyperclip`
* **Network:** `requests`

## ⚙️ Setup & Installation
1. Ensure you have Python and `uv` installed.
2. Clone this repository:
   ```bash
   git clone https://github.com/Islamdagher2092/Vision-Desktop-Automation.git
   ```
3. Sync the dependencies using `uv`:
   ```bash
   uv sync
   ```

## 🎯 Usage
Run the main script to start the automation workflow:
```bash
uv run main.py
```
*The script will automatically scan the screen, draw bounding boxes (saved in `annotated_screenshots/`), fetch data, type it into Notepad, and save the files to the designated target directory.*