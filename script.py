#TODO create docker image for this project for easier pull
#TODO wrap tool into a function with try: and except:
#TODO add the ability to search for multiple locations in one script run
#TODO add the ability to customize the options selected on myturn.ca.gov for disability/location/age/occupation, etc
#TODO add the ability to use other notification methods
#TODO test/document running Docker image on Crostini
#TODO test on slimmer Docker image such as Alpine
#TODO test on RasPi arm processors
#TODO split out Dockerfile skeleton to its own github repo for cron jobs on Docker 

import sys
import time
import configparser
import http.client
import urllib
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

print("Program succesfully started!")

#ConfigParser configuration
config = configparser.ConfigParser()
config.read('/app/config.ini')

#ConfigParser myturn.ca.gov variables import
url = config.get('myturn.ca.gov', 'WebsiteURL')
location = config.get('myturn.ca.gov', 'MyLocation')

#Config Parser Pushover Credentials Import
pushover_user = config.get('pushover.net', 'PushoverUser')
pushover_token = config.get('pushover.net', 'PushoverToken')

print("Config file successfully read!")

#Selenium config
opts = Options()  # options for chromedriver
opts.add_argument("--window-size=800,1080")  # specifies window width,height
opts.add_argument("user-agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36")
opts.add_argument("headless")  # runs without the browser visible
#opts.add_argument("disable-gpu")  # runs without the browser visible
opts.add_argument("--no-sandbox")

#Pushover config
conn = http.client.HTTPSConnection('api.pushover.net:443')

# initialize chromedriver global variable.
chromedriver = None

#Point the script to the location of chromedriver using 'whereis chromedriver' in termial window
chromedriver = webdriver.Chrome(executable_path='/usr/bin/chromedriver', options=opts)

def main():
    #Load the URL and wait for it to load
    try:
        chromedriver.get(url)
    except:
        print("An exception occurred")
    else:
        time.sleep(5)
        #Click 'Register and check my eligibility'
        proceed_page1 = chromedriver.find_element_by_xpath('//*[@id="root"]/div/main/div[1]/div/div[2]/div[3]/button')
        proceed_page1.click()
        #Certify 18+ age
        age = chromedriver.find_element_by_xpath('//*[@id="q-screening-18-yr-of-age"]')
        age.click()
        #Certify information is true and accurate
        certify = chromedriver.find_element_by_xpath('//*[@id="q-screening-health-data"]')
        certify.click()
        #Attest to accuracy of information
        attest = chromedriver.find_element_by_xpath('//*[@id="q-screening-accuracy-attestation"]')
        attest.click()
        #Accept Privacy Statement
        privacy = chromedriver.find_element_by_xpath('//*[@id="q-screening-privacy-statement"]')
        privacy.click()
        #Select age range from given options
        select_age = chromedriver.find_element_by_xpath('//*[@id="root"]/div/main/div/form/span[5]/div/fieldset/div[2]/label[1]')
        select_age.click()
        #Select health conditions
        select_conditions = chromedriver.find_element_by_xpath('//*[@id="root"]/div/main/div/form/span[6]/div/fieldset/div[3]/label[1]')
        select_conditions.click()
        #Select disability
        select_disability = chromedriver.find_element_by_xpath('//*[@id="root"]/div/main/div/form/span[7]/div/fieldset/div[2]/label[2]')
        select_disability.click()
        #Select industry
        select_industry = chromedriver.find_element_by_xpath('//*[@id="q-screening-eligibility-industry"]/option[3]')
        select_industry.click()
        #Select county
        select_county = chromedriver.find_element_by_xpath('//*[@id="q-screening-eligibility-county"]/option[47]')
        select_county.click()
        #Proceed to next page
        proceed_page2 = chromedriver.find_element_by_xpath('/html/body/div[1]/div/main/div/form/div/button[1]')
        proceed_page2.click()
        time.sleep(3)
        #Enter location
        enter_zip = chromedriver.find_element_by_xpath('//*[@id="location-search-input"]')
        enter_zip.send_keys(location)
        enter_zip.send_keys(Keys.ENTER)
        #Hit submit button (this isn't needed right now because the 'ENTER' in the previous code block submits to the next page
        #proceed_page3 = chromedriver.find_element_by_xpath('/html/body/div[1]/div/main/div/div[5]/button[1]')
        #proceed_page3.click()
        #Print page results entirely for debugging
        #print(chromedriver.page_source)
        #Wait for next page to fully load before taking screenshot
        time.sleep(5)
        if chromedriver.find_elements_by_css_selector('#root > div > main > div.tw-max-w-screen-sm.tw-p-6.tw-mx-auto.md\:tw-px-0.tw-pt-8 > div.tw-space-y-4 > div > h2'):
            print("No appointments are available")
        else:
            chromedriver.save_screenshot("appointments.png")
            print("Appointments are available for " + location)
            r = requests.post("https://api.pushover.net/1/messages.json", data = {
                "token": pushover_token,
                "user": pushover_user,
                "message": "Appointments are available for " + location,
            },
            files = {
                "attachment": ("image.png", open("appointments.png", "rb"), "image/png")
            })
     
        chromedriver.quit()

# process main method call
if __name__ == '__main__':
    main()
