#Base on this tutorial https://youtu.be/Rg29fnSGc5U
#pip install selenium
#pip install web
#pip install ?ikernelpy? something
from time import sleep
from selenium import webdriver-manager
from webdriver_manager.chrome import ChromeDriverManager

driver=webdriver.Chrome(ChromeDriverManager().install())
driver.maximize_window()
driver.get("https://www.twitch.tv/popout/openmacroinput/chat")
print("Application title is ", driver.title)
print("Application url is ", driver.current_url)

#sleep(500)
#driver.quit()
