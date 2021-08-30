import csv
from selenium import webdriver
from selenium.common import exceptions
import sys
import time
from random import randint
import requests
from selenium.webdriver.common.keys import Keys

#open chrome browser
driver = webdriver.Chrome()

def login():
	# ADD site Url here to login
	driver.get ("https://www.instagram.com/")  

	time.sleep(5)

	username = driver.find_element_by_name("username")

	# To clear Already Exsisting username or email
	username.clear()

	user = "muhammad_ibrahim_anjum" #input("Enter Instagram UserName: \n")

	# Insert UserName or Email
	username.send_keys(user)

	# get password element after inspecting on chrome
	Password = driver.find_element_by_name("password")

	# To clear Already Exsisting Passwords
	Password.clear()

	pwd = 'Ibmkhan1994'#input("Enter Password: \n")

	# Insert Password key
	Password.send_keys(pwd)

	# click button to login
	driver.find_element_by_xpath('//button[@type="submit"]').click()

	time.sleep(5)

	# notNow = driver.find_element_by_xpath("//*[contains(text(), 'Not Now')]")

	# if(notNow):
	# 	notNow.click()

    
	if driver.find_element_by_xpath("//*[contains(text(), 'Not Now')]"):
	    driver.find_element_by_xpath("//*[contains(text(), 'Not Now')]").click()
	# wait until it loads home page
	#WebDriverWait(driver, 10).until(EC.find_element_by_xpath('//*[name()="svg"][@aria-label="Home"]'))

login()

time.sleep(5)

def getFollowings():
    with open('instFollowing.csv' , 'w') as f:
        fieldnames = ['Following Profiles']
        thewriter = csv.DictWriter(f, fieldnames=fieldnames)
        thewriter.writeheader()
    avtar = driver.find_element_by_xpath('//div[@class="Fifk5"]//img[@data-testid="user-avatar"]')
    avtar.click()
    time.sleep(0.5)
    profile = driver.find_element_by_xpath('//div[@class="_01UL2"]/a//*[contains(text(), "Profile")]')
    profile.click()
    time.sleep(5)
    followingList = driver.find_element_by_xpath('//section[@class="zwlfE"]/ul/li[2]')
    followingList.click()

    time.sleep(5)
    
    followingLinks = driver.find_elements_by_xpath('//li[@class="wo9IH"]/div/div/div/div/span/a/@href')

    for link in followingLinks:
        print(link)
        with open('instFollowing.csv' , 'a', newline='' , encoding = 'utf-8' ) as f:
            fieldnames = ['Following Profiles']
            thewriter = csv.DictWriter(f, fieldnames=fieldnames)
            thewriter.writerow({'Following Profiles' : link })
getFollowings()