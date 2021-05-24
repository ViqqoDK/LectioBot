from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
import secrets
import sqlite3

# HOW TO RUN: python3 lectiobot.py

# Define database
db_file = r"students.db"

# 
# In this case, 33 is Virum Gymnasium. Make sure to change this for your school.
school_ID = "33"     
webdriver_path = "webdrivers/chromedriver.exe"

class LectioBot:
    def __init__(self, username, pw):
        #self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(webdriver_path)
        self.driver.get("https://www.lectio.dk/lectio/"+school_ID+"/login.aspx?prevurl=FindSkema.aspx%3ftype%3delev")
        self.driver.find_element_by_id('username')\
            .send_keys(username)
        self.driver.find_element_by_id('password')\
            .send_keys(pw)
        sleep(0.1)
        self.driver.find_element_by_id('m_Content_submitbtn2')\
            .click()

        Letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "Æ", "Ø", "Å"]
        # Go to next letter A -> B -> ... -> Ø -> Å
        StudentTable = "https://www.lectio.dk/lectio/33/FindSkema.aspx?type=elev&forbogstav="
        Profiles = []

        # Go through each menu 
        for letter in Letters:
            Cursor = StudentTable
            Cursor += letter
            self.driver.get(f"{Cursor}")
            
            # Get names and ID
            Persons = self.driver.find_element_by_id('m_Content_listecontainer')
            links = Persons.find_elements_by_tag_name('a')

            for link in links:
                temp = link.text.split(" (")
                if len(temp) != 2:
                    Profiles.append([temp[0], "", ""])
                else:
                    name = temp[0]
                    studentClass = temp[1].split(" ")[0]      
                    studentID = link.get_attribute("href").split("studentID=")[1]
                    Profiles.append([name, studentClass, studentID])

        print(Profiles)

        # Save names to file
        csvfile = "output/profiles/studentInfo.txt"
        f = open(csvfile, "w")
        for person in Profiles:
            f.write(f"{person[0]}, {person[1]}, {person[2]}\n")


        self.driver.quit()


bot = LectioBot(secrets.username, secrets.pw)
