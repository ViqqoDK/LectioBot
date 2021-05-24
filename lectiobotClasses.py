from selenium import webdriver
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
    def SaveName(self, StudentID, ClassID, ImageID):
        # Save names to file
        csvfile = "output/profiles/studentInfo5.txt"
        with open(csvfile, "a") as f:
            f.write(f"{StudentID}, {ClassID}, {ImageID}\n")

    def SaveImage(self, StudentID, ImageID):
        # Iterate over the ImageIDs and take a screenshot
        self.driver.get(f"{ImageID}")
        screenshot = self.driver.get_screenshot_as_png()

        # Crop image
        im = Image.open(BytesIO(screenshot))
        left = 535
        top = 504
        right = 715
        bottom = 744
        im = im.crop((left, top, right, bottom))
        im.save(f"output/pictures/byPersonID/{StudentID}.png")


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

        # Lists
        Classes = []
        Students = []

        # Iterate over the classlist to get each ClassID
        Parent = self.driver.find_element_by_id('m_Content_listecontainer')
        Classlinks = Parent.find_elements_by_tag_name('a')
        for link in Classlinks:
            Classes.append(link.get_attribute("href").split("klasseid=")[1])

        # Iterate over each class to get images 
        for ClassID in Classes:
            # Go to class site
            self.driver.get(f"https://www.lectio.dk/lectio/33/subnav/members.aspx?klasseid={ClassID}&showstudents=1")
            # Select better image quality CheckBox
            self.driver.find_element_by_id("s_m_Content_Content_IsPrintingHiResPicturesCB").click()
            
            # Get StudentID and ImageID
            Persons = self.driver.find_element_by_id('s_m_Content_Content_list')
            Images = Persons.find_elements_by_tag_name('img')
            PersonLink = Persons.find_elements_by_tag_name('a')

            ImageIDs = []
            PersonIDs = []
            for Image, PersonID in zip(Images, PersonLink[4::]):
                ImageIDs.append(Image.get_attribute("src"))
                PersonIDs.append(PersonID.get_attribute("href").split("studentID=")[1])
            

            for s in range(len(ImageIDs)):
                # Save names to a csvfile
                #self.SaveName(PersonIDs[s], ClassID, ImageIDs[s])
                # Save images of students
                self.SaveImage(PersonIDs[s], ImageIDs[s])

        print("SUCCES!!!")
        self.driver.quit()
        exit()
    

bot = LectioBot(secrets.username, secrets.pw)
