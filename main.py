import time
import os
import requests
import pyautogui
import pygetwindow as gw
import pyperclip
from grounder import IconGrounder

# إعدادات عامة
API_URL = "https://jsonplaceholder.typicode.com/posts"
TARGET_DIR = os.path.join(os.path.expanduser("~"), "Desktop", "tjm-project")

# إعداد المجلد الهدف
os.makedirs(TARGET_DIR, exist_ok=True)
# جعل حركة الماوس أكثر طبيعية لتجنب الأخطاء
pyautogui.PAUSE = 0.5 

def fetch_posts(limit=10):
    """جلب المنشورات من الـ API مع معالجة أخطاء الاتصال (Graceful Degradation)"""
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(API_URL, headers=headers, timeout=15)
        response.raise_for_status()
        return response.json()[:limit]
    except requests.RequestException as e:
        print(f"\n[Warning] Error fetching API: {e}")
        print("[Info] API is unavailable. Initiating Graceful Degradation using local dummy data...\n")
        
        # إنشاء بيانات وهمية بديلة لإكمال مسار الأتمتة
        dummy_posts = []
        for i in range(1, limit + 1):
            dummy_posts.append({
                "id": i,
                "title": f"Fallback Local Title {i}",
                "body": f"This is local offline content for post {i}. The main API was unreachable, triggering graceful degradation."
            })
        return dummy_posts

def launch_notepad(grounder: IconGrounder, retries=3) -> bool:
    """محاولة فتح Notepad باستخدام الـ Vision Grounding مع Retry Logic"""
    for attempt in range(retries):
        print(f"Attempt {attempt + 1}: Searching for Notepad icon...")
        coords = grounder.locate_icon_by_text("Notepad")
        
        if coords:
            x, y = coords
            print(f"Icon grounded at (X: {x}, Y: {y}). Clicking...")
            pyautogui.moveTo(x, y, duration=0.5)
            pyautogui.doubleClick()
            
            # التحقق من أن النافذة فتحت بالفعل
            time.sleep(2) # انتظار تحميل البرنامج
            windows = gw.getWindowsWithTitle("Notepad")
            if windows:
                print("Notepad launched successfully.")
                windows[0].activate()
                return True
            else:
                print("Clicked, but Notepad window not detected. Retrying...")
        else:
            print("Notepad icon not found on screen. Retrying in 1 second...")
            time.sleep(1)
            
    print("Failed to launch Notepad after maximum retries.")
    return False

def process_post(post, grounder):
    """مسار العمل لكل منشور"""
    if not launch_notepad(grounder):
        return

    # انتظار حتى يفتح النوت باد ويستقر
    time.sleep(1.5) 
    
    # [حل مشكلة ويندوز 11]: تحديد أي نص قديم ومسحه لضمان صفحة نظيفة
    pyautogui.hotkey('ctrl', 'a')
    time.sleep(0.2)
    pyautogui.press('backspace')
    time.sleep(0.2)
    
    # مسار الملف والتحقق من وجوده مسبقاً لمسحه
    file_path = os.path.join(TARGET_DIR, f"post_{post['id']}.txt")
    if os.path.exists(file_path):
        os.remove(file_path)
    
    # تجهيز المحتوى
    title = post.get("title", "")
    body = post.get("body", "")
    content = f"Title: {title}\n\n{body}"
    
    print(f"Typing post {post['id']}...")
    
    # لصق المحتوى
    pyperclip.copy(content)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(1) # ننتظر ثانية لضمان اكتمال اللصق
    
    # [حل مشكلة الحفظ]: استخدام Save As والانتظار فترة كافية لظهور النافذة
    pyautogui.hotkey('ctrl', 'shift', 's')
    time.sleep(2) # مهم جداً: انتظار ثانيتين لضمان ظهور نافذة الحفظ
    
    # لصق مسار الملف في نافذة الحفظ
    pyperclip.copy(file_path)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.5)
    pyautogui.press('enter')
    
    # انتظار حتى تكتمل عملية الحفظ فعلياً
    time.sleep(1.5)
    
    # إغلاق النوت باد إجبارياً لضمان عدم تداخله مع المنشور التالي
    os.system("taskkill /f /im notepad.exe >nul 2>&1")
    print(f"Post {post['id']} saved and Notepad closed forcefully.\n")
    time.sleep(1) # راحة قصيرة قبل الدورة القادمة

def main():
    print("Starting Vision-Based Desktop Automation...")
    grounder = IconGrounder()
    
    posts = fetch_posts(limit=10)
    if not posts:
        print("No posts to process. Exiting.")
        return

    for post in posts:
        process_post(post, grounder)
        
    print("Automation workflow completed successfully!")

if __name__ == "__main__":
    main()