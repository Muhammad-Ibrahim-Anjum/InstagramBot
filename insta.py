import csv
from selenium import webdriver
from selenium.common import exceptions
import sys
import time
from random import randint
import requests
from selenium.webdriver.common.keys import Keys
import random

#open chrome browser
driver = webdriver.Firefox()

def login():
	# ADD site Url here to login
	driver.get ("https://www.instagram.com/")  

	time.sleep(5)

	username = driver.find_element_by_name("username")

	# To clear Already Exsisting username or email
	username.clear()

	user = 'ibrahimAnjum'#input("Enter Instagram UserName: \n")

	# Insert UserName or Email
	username.send_keys(user)

	# get password element after inspecting on chrome
	Password = driver.find_element_by_name("password")

	# To clear Already Exsisting Passwords
	Password.clear()

	pwd = '12345'#input("Enter Password: \n")

	# Insert Password key
	Password.send_keys(pwd)

	# click button to login
	driver.find_element_by_xpath('//button[@type="submit"]').click()

login()

time.sleep(2)
links = []
def getPostLinks(NumOfPosts):
    # # Get scroll height
    # last_height = driver.execute_script("return document.body.scrollHeight")

    # while True:
    #     # Scroll down to bottom
    #     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    #     time.sleep(7)

    #     # Calculate new scroll height and compare with last scroll height
    #     new_height = driver.execute_script("return document.body.scrollHeight")
    #     if new_height == last_height:
    #         break
    #     last_height = new_height

    #     posts = driver.find_elements_by_xpath("//a[@tabindex='0']")
    #     totalPosts = len(posts)
    #     for i in range(totalPosts):
    #         if len(links) < NumOfPosts:
    #             postUrl = posts[i].get_attribute("href")
    #             links.append(postUrl)
    #         break

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    for hight in range(1,NumOfPosts):
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        time.sleep(3)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
        
    time.sleep(3)

    posts = driver.find_elements_by_xpath("//a[@tabindex='0']")
    numOfPosts = len(posts)
    for i in range(numOfPosts):
        postUrl = posts[i].get_attribute("href")
        links.append(postUrl)

        
    time.sleep(3)


def likeOnly(links):
    for url in links:
        driver.get(url)
        try:
            time.sleep(5)
            try:
                if driver.find_element_by_xpath('//*[name()="svg"][@aria-label="Like"] [@height="24"]'):
                    like = driver.find_element_by_xpath('//*[name()="svg"][@aria-label="Like"] [@height="24"]//ancestor::div[1]')
                    like.click()
                    print("You have Liked a Post")
            except:
                print("You Already Liked this Post")
                continue
        except:
            print('Link Not Working')
            continue
            

def commentOnly(links, comment, comment1, comment2):
    for url in links:
        driver.get(url)
        try:
            time.sleep(2)
            commentArea = driver.find_element_by_xpath('//form/textarea[@aria-label="Add a comment…"]')
            commentArea.click()
            commentList = [comment, comment1, comment2]
            comment = random.choice(commentList)
            comment = comment+u' \U0001F970' + u'\U0001F60D' #use unicodes here!
            time.sleep(2)
            commentArea = driver.find_element_by_xpath('//form/textarea[@aria-label="Add a comment…"]')
            time.sleep(1)
            commentArea.send_keys(comment)
            post = driver.find_element_by_xpath('//form/button[@type="submit"]')
            post.click()
            time.sleep(3)
        except:
            print('Link Not Working')
            continue

def LikeAndComment(links, comment, comment1, comment2):
    for url in links:
        driver.get(url)
        try:
            time.sleep(5)
            try:
                if driver.find_element_by_xpath('//*[name()="svg"][@aria-label="Like"][@height="24"]'):
                    like = driver.find_element_by_xpath('//*[name()="svg"][@aria-label="Like"][@height="24"]//ancestor::div[1]')
                    like.click()
                    print("You have Liked a Post")
            except:
                print("You Already Liked this Post")
                pass

            time.sleep(2)
            commentList = [comment, comment1, comment2]
            comment = random.choice(commentList)
            comment = comment+u' \U0001F970' + u'\U0001F60D' #use unicodes here!
            commentArea = driver.find_element_by_xpath('//form/textarea[@aria-label="Add a comment…"]')
            commentArea.click()
            time.sleep(2)
            commentArea = driver.find_element_by_xpath('//form/textarea[@aria-label="Add a comment…"]')
            commentArea.send_keys(comment)
            post = driver.find_element_by_xpath('//form/button[@type="submit"]')
            time.sleep(1)
            post.click()
            time.sleep(3)
        except:
            print('Link Not Working')
            continue

def likeComments(links):
    for url in links:
        driver.get(url)
        try:
            time.sleep(5)
            try:
                if driver.find_element_by_xpath('//*[name()="svg"][@aria-label="Like"][@height="12"]'):
                    cmntLikes = driver.find_elements_by_xpath('//*[name()="svg"][@aria-label="Like"][@height="12"]')
                    for like in cmntLikes:
                        cmntLike = like.find_element_by_xpath('//*[name()="svg"][@aria-label="Like"][@height="12"]//ancestor::div[1]')
                        cmntLike.click()
                        print("You have Liked a Comment")
            except:
                print("This Post Don't have any Comments")
                continue
        except:
            print('Link Not Working')
            continue

def scrapPosts(links):
    time.sleep(3)
    with open('scrapedPosts.csv' , 'w', newline='') as f:
        fieldnames = ['Url' , 'Images' , 'Details' , 'Likes & Views' , 'Time of Post']
        thewriter = csv.DictWriter(f, fieldnames=fieldnames)
        thewriter.writeheader()

    for link in links:
        driver.get(link)
        try:
            time.sleep(randint(3,5))
            try:
                image = driver.find_element_by_xpath('//div[@class="_97aPb wKWK0"]//child::img').get_attribute('src')
                print(image)
            except:
                try:
                    image = driver.find_element_by_xpath('//div[@class="_97aPb wKWK0"]//child::video').get_attribute('src')
                    print(image)
                except:
                    image = 'Broken Image'
                
            details = driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div[1]/article/div[3]/div[1]/ul/div/li/div/div/div[2]/span').text
            print(details)
            try:
                likes = driver.find_element_by_xpath("//*[@id='react-root']/section/main/div/div[1]/article/div[3]/section[2]/div/div/a").text
                print(likes)            
            except:
                try:
                    likes = driver.find_element_by_xpath("//*[@id='react-root']/section/main/div/div[1]/article/div[3]/section[2]/div/span").text
                    print(likes)
                except:
                    likes = '0 Likes'
            timeOfPost = driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div[1]/article/div[3]/div[2]/a/time').get_attribute('title')
            print(timeOfPost)
            with open('scrapedPosts.csv' , 'a' , newline='', encoding = 'utf-8' ) as f:
                fieldnames = ['Url' , 'Images','Details' , 'Likes & Views' , 'Time of Post']
                thewriter = csv.DictWriter(f, fieldnames=fieldnames)
                thewriter.writerow({'Url' : link , 'Images' : image , 'Details' : details , 'Likes & Views' : likes , 'Time of Post' : timeOfPost})
        except:
            print("page not found or link is broken")
            continue

print("""
***************** Select Following Options ********************

1 - Tags

2 - Profiles

""")

while(True):
    option = int(input("Select One of Above Options : "))
    if option == 1:
        hashTag = input("Enter HashTag Without #: \n")
        NumOfPosts = int(input('Number of Posts? : '))
        driver.get('https://www.instagram.com/explore/tags/'+ hashTag + '/')
        print("wait until it loads Post for HashSTag "+hashTag)
        time.sleep(randint(3,5))
        getPostLinks(NumOfPosts)
        break
    elif option == 2:
        profile = input("Enter Profile Name (User Name): \n")
        NumOfPosts = int(input('Number of Posts? : '))
        driver.get('https://www.instagram.com/'+ profile + '/')
        print("wait until it loads Post for "+profile)
        time.sleep(randint(3,5))
        getPostLinks(NumOfPosts)
        break


print("""
***************** Select Following Options ********************

1 - Like Posts Only

2 - Comment Posts Only

3 - Like and Comment (Both)

4 - Like Comments Only

5 - Scrap Posts

""")

while(True):
    option = int(input("Select One of Above Options : "))
    if option == 1:
        likeOnly(links)
        break
    elif option == 2:
        comment = input('Please Write Your Comment Below : \n')
        comment1 = input('Please Write Your Comment Below : \n')
        comment2 = input('Please Write Your Comment Below : \n')
        commentOnly(links,comment,comment1,comment2)
        break
    elif option == 3:
        comment = input('Please Write Your Comment Below : \n')
        comment1 = input('Please Write Your Comment Below : \n')
        comment2 = input('Please Write Your Comment Below : \n')
        LikeAndComment(links,comment,comment1,comment2)
        break
    elif option == 4:
        likeComments(links)
        break
    elif option == 5:
        scrapPosts(links)
        break

driver.close()
