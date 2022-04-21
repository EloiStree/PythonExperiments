import pyautogui

print(pyautogui.size())
a=(0,840,620,240)
#pos = pyautogui.locateOnScreen('Test.png', grayscale=True, confidence=0.70)
pos = pyautogui.locateOnScreen('Test.png',region=a)
#pos = pyautogui.locateOnScreen('Test.png', grayscale=True, confidence=0.70)
im= pyautogui.screenshot('my_screenshot.png',region=a)
if (pos != None):
   x, y = pyautogui.center(pos)
   pyautogui.click(x, y)
   print('Yo')
   