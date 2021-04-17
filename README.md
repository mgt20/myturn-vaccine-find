# myturn-vaccine-find

This is a python3 script that can be run inside or outside of Docker on a cron schedule to scrape the myturn.ca.gov website for COVID-19 vaccination locations with potentially available appointment times. Notifications for potential sites with appointments will appear on the printed output in the command line terminal. There is also support for pushover.net's API for push notifications. NOTE: Pushover is a ~$5 purchase to unlock, but there may be a trial available. There are plans to support other notification methods in the future.

This has been tested on x86 CPUs and ARM (e.g. Raspberry Pi) CPUs.

## Required services
1. Pushover (this should be a one-time fee in the mobile phone app stores). Currently, appointment site matches are printed to the console. Pushover is used to send push notifications of these matches to a mobile device. Once purchased, export a user key and a token for use in the config.ini file within this repository.

## To download
1. Clone this repository into a working folder using 'git clone https://github.com/mgt20/myturn-vaccine-find.git'. Or, download using the GitHub WebGUI.

## To customize the script configuration
1. Rename config.sample.ini to config.ini
2. Modify Dockerfile with your timezone (make sure to use a supported Timezone syntax/variable).
3. Modify cronjobs file with your desired cron schedule. See crontab.guru for help with this.
4. Modify config.ini file, section "myturn.ca.gov", with the xpath values for the age range, health conditions, disabilities, work industry, and county that apply to you. You can use the Chrome Browser's "Inspect" function to find the xpath for the option that applies to you while stepping through myturn.ca.gov.
5. Modify the config.ini file, section "myturn.ca.gov Locations", with your Location as entered on the "Enter your address or zip code" field of myturn.ca.gov. Important: Enter this exactly as entered on the website. If you'd like to search for more locations, add a row for additional locations with a unique name like "MyLocation3" or MyLocation4".
6. Modify the config.ini file, section "pushover.net", with your pushover user and token keys.

## To run on baremetal / without Docker
1. Install the required dependencies on your machine (see Dockerfile for OS packages needed and see requirements.txt for required pip packages).
2. Update the path for chromedriver in script.py based on where it is on your machine (for Linux systems, you can run 'whereis chromedriver' to find this out). 
3. In script.py, you will need to update the path for config.ini from '/app/config.ini' to 'config.ini'
4. Run the script by running: 'python3 script.py' while in the folder of the downloaded repository on your machine. You can comment out the headless option for Selenium if you'd like to see the script open and navigate a webpage.

## To run on Docker
1. Have Docker and docker-compose installed and configured for use.
2. Run: 'docker-compose up --build" while in the working directory that houses the files downloaded from github to run the container. Optional: To run in "detached" mode instead (no print to console with process dependent on terminal window), instead run with -d flag added, such as: 'docker-compose up --build -d'

NOTES:
1. The current schedule runs the script hourly at the 1st minute of every hour (ex. 6:01pm, 7:01pm, etc). If you modify the cronjobs file, make sure to leave a blank line at the end of the file.
