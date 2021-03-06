#TODO create docker image for this project for easier pull
#TODO Use GET or POST instead of browser automation
#TODO add the ability to use other notification methods
#TODO test/document running Docker image on Crostini
#TODO test on slimmer Docker image such as Alpine
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
from selenium.common.exceptions import SessionNotCreatedException

print("Program succesfully started!")

#ConfigParser configuration
config = configparser.ConfigParser()
config.read('/app/config.ini')
#config.read('config.ini')

url = ('https://myturn.ca.gov')

#ConfigParser myturn.ca.gov variables import
location_items = config.items("myturn.ca.gov Locations")
privacy_accept = config.get('myturn.ca.gov', 'PrivacyAccept')
my_age = config.get('myturn.ca.gov', 'MyAge')
my_county = config.get('myturn.ca.gov', 'MyCounty')
work_in_diff_county = config.get('myturn.ca.gov', 'WorkInDiffCounty')
certify_my_age = config.get('myturn.ca.gov', 'CertifyMyAge')
certify_info = config.get('myturn.ca.gov', 'CertifyInfo')

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

def main():
    for key, location in location_items:
        #Load the URL and wait for it to load
        chromedriver = None
        chromedriver = webdriver.Chrome(executable_path='/usr/bin/chromedriver', options=opts)
        try:
            chromedriver.get(url)
        except Exception as e:
            print(e)
            sys.exit(1)
        else:
            time.sleep(5)
            #Click 'Register and check my eligibility' then proceed to next page
            chromedriver.find_element_by_xpath('//*[@id="root"]/div/main/div[1]/div/div[2]/div[3]/button').click()
            #Accept Privacy Statement
            chromedriver.find_element_by_css_selector(privacy_accept).click()
            #18+ age
            chromedriver.find_element_by_css_selector(my_age).click()
            #Select county
            chromedriver.find_element_by_css_selector(my_county).click()
            #Live and work in same county 
            chromedriver.find_element_by_css_selector(work_in_diff_county).click() 
            #Certify 18+ age
            chromedriver.find_element_by_css_selector(certify_my_age).click()
            #Certify information is true and accurate
            chromedriver.find_element_by_css_selector(certify_info).click()
            #Proceed to next page
            chromedriver.find_element_by_xpath('/html/body/div[1]/div/main/div/form/div/button[1]').click()
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
