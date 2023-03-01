from selenium import webdriver 
from selenium.webdriver.chrome.options import Options
import time 

def main():
    options = Options()
    options.add_argument("--kiosk")
    driver = webdriver.Chrome(options=options)
    driver.get('http://127.0.0.1:5000/')
    while True:
        pass
    #time.sleep(10)
    #driver.quit()


if __name__ == '__main__':
    main()
