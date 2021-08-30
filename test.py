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

class login:
    def loginAccount(self):
        # ADD site Url here to login
        driver.get ("https://www.instagram.com/")  

        time.sleep(5)

        username = driver.find_element_by_name("username")

        # To clear Already Exsisting username or email
        username.clear()

        user = 'muhammad_ibrahim_anjum'#input("Enter Instagram UserName: \n")

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

        # wait until it loads home page
        #WebDriverWait(driver, 10).until(EC.find_element_by_xpath('//*[name()="svg"][@aria-label="Home"]'))


class AccessPages:
    def __init__(self):
        self.links = []

    def getPostLinks(self):
        # Get scroll height
        last_height = driver.execute_script("return document.body.scrollHeight")

        for hight in range(1,3):
            # Scroll down to bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            time.sleep(7)

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
            self.links.append(postUrl)

time.sleep(2)

class PostActions(AccessPages):
    @staticmethod
    def likeOnly(Pageslinks):
        for url in Pageslinks.links:
            driver.get(url)
            time.sleep(5)
            try:
                if driver.find_element_by_xpath('//*[name()="svg"][@aria-label="Like"] [@height="24"]'):
                    like = driver.find_element_by_xpath('//*[name()="svg"][@aria-label="Like"] [@height="24"]//ancestor::div[1]')
                    like.click()
                    print("You have Liked a Post")
            except:
                print("You Already Liked this Post")
                continue
    
    @staticmethod
    def commentOnly(Pageslinks):
        for url in Pageslinks.links:
            driver.get(url)
            time.sleep(5)
            cmnt = input("Enter Comment: \n")
            comment = driver.find_element_by_xpath("//form/textarea")
            comment.click()
            time.sleep(2)
            comment = driver.find_element_by_xpath("//form/textarea")
            comment.send_keys(cmnt)
            post = driver.find_element_by_xpath("//form/button")
            post.click()

    @staticmethod
    def LikeAndComment(Pageslinks):
        for url in Pageslinks.links:
            driver.get(url)
            time.sleep(5)
            try:
                if driver.find_element_by_xpath('//*[name()="svg"][@aria-label="Like"][@height="24"]'):
                    like = driver.find_element_by_xpath('//*[name()="svg"][@aria-label="Like"][@height="24"]//ancestor::div[1]')
                    like.click()
                    print("You have Liked a Post")
            except:
                print("You Already Liked this Post")
                continue

            time.sleep(2)
            cmnt = input("Enter Comment: \n")
            comment = driver.find_element_by_xpath("//form/textarea")
            comment.click()
            time.sleep(2)
            comment = driver.find_element_by_xpath("//form/textarea")
            comment.send_keys(cmnt)
            post = driver.find_element_by_xpath("//form/button")
            post.click()

    @staticmethod
    def likeComments(Pageslinks):
        for url in Pageslinks.links:
            driver.get(url)
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

    @staticmethod
    def searchHashTags(Pageslinks):
        time.sleep(3)
        with open('scrapedPosts.csv' , 'w', newline='') as f:
            fieldnames = ['Url' , 'Images' , 'Details' , 'Likes & Views' , 'Time of Post']
            thewriter = csv.DictWriter(f, fieldnames=fieldnames)
            thewriter.writeheader()

        for link in Pageslinks.links:
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

login = login()
login.loginAccount()

print("""
***************** Select Following Options ********************

1 - Tags

2 - Profiles

""")

while(True):
    option = int(input("Select One of Above Options : "))
    if option == 1:
        hashTag = input("Enter HashTag Without #: \n")
        driver.get('https://www.instagram.com/explore/tags/'+ hashTag + '/')
        print("wait until it loads Post for HashSTag")
        time.sleep(10)
        getAllLinks = AccessPages()
        getAllLinks.getPostLinks()
        break
    elif option == 2:
        profile = input("Enter Profile Name (User Name): \n")
        driver.get('https://www.instagram.com/'+ profile + '/')
        print("wait until it loads Post for HashSTag")
        time.sleep(10)
        getAllLinks = AccessPages()
        getAllLinks.getPostLinks()
        break

print("""
***************** Select Following Options ********************

1 - Like Posts Only

2 - Comment Posts Only

3 - Like and Comment (Both)

4 - Like Comments Only

5 - Scrap Posts With hash Tags

""")

while(True):
    option = int(input("Select One of Above Options : "))
    if option == 1:
        postLinks = AccessPages()
        PostActions.likeOnly(postLinks)
        break
    elif option == 2:
        postLinks = AccessPages()
        PostActions.commentOnly(postLinks)
        break
    elif option == 3:
        postLinks = AccessPages()
        PostActions.LikeAndComment(postLinks)
        break
    elif option == 4:
        postLinks = AccessPages()
        PostActions.likeComments(postLinks)
        break
    elif option == 5:
        postLinks = AccessPages()
        PostActions.searchHashTags(postLinks)
        break

driver.close()