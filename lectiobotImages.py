from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from time import sleep
from PIL import Image
from io import BytesIO
import secrets
import sqlite3

# HOW TO RUN: python3 lectiobot.py

# Define database
db_file = r"students2.db"

class LectioBot:
    def __init__(self, username, pw):
        # Start driver
        self.driver = webdriver.Chrome('webdrivers/chromedriver.exe')
        # Go to site
        self.driver.get("https://www.lectio.dk/lectio/33/FindSkema.aspx?type=stamklasse")
        # Login
        self.driver.find_element_by_id('username')\
            .send_keys(username)
        self.driver.find_element_by_id('password')\
            .send_keys(pw)
        sleep(0.1)
        self.driver.find_element_by_id('m_Content_submitbtn2')\
            .click()

        # Iterate over the ImageIDs and take a screenshot
        self.driver.get("https://www.lectio.dk/lectio/33/GetImage.aspx?pictureid=43256633584&fullsize=1")
        screenshot = self.driver.get_screenshot_as_png()
        self.driver.quit()

        im = Image.open(BytesIO(screenshot))
        left = 535
        top = 504
        right = 715
        bottom = 744

        im = im.crop((left, top, right, bottom))
        im.save("output/pictures/test/test3.png")



bot = LectioBot(secrets.username, secrets.pw)


