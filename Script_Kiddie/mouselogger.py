import pyautogui

def mouseLogger():
    x, y = pyautogui.position()
    print("Mouse Position - X:", x, "Y:", y)
    
while True:
    mouseLogger()