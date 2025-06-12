import os
import pyautogui

def screenshot(path:str=""):
    if path:
        if not path.lower().endswith('.png'):
            path += ".png"
    else:
        path = os.path.join(os.getcwd(), 'screenshot')
        if not os.path.exists(path):
            os.makedirs(path)
        path = os.path.join(path, 'screenshot.png')
        
    pyautogui.screenshot(path)
    return path
        
    
if __name__ == "__main__":
    print(screenshot())