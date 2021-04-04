# myturn-vaccine-find

This is a python3 script that can be run inside or outside of Docker on a cron schedule to scrape the myturn.ca.gov website for COVID-19 vaccination locations with potentially available appointment times. Notifications for potential sites with appointments will appear on the printed output in the command line terminal. There is also support for pushover.net's API for push notifications. NOTE: Pushover is a ~$5 purchase to unlock, but there may be a trial available.

## To setup this script with Docker
1. Have Docker and docker-compose installed and configured for use.
2. Clone this repository into a working folder using 'git clone https://github.com/mgt20/myturn-vaccine-find.git'
3. Rename config.sample.ini to config.ini
4. Modify the config.ini file with your values for: pushover.net user and token. These can be obtained after creating an account on pushover.net
5. Run: 'docker-compose up --build" while in the working directory that houses the files downloaded from github to run the container.

NOTES:
1. The current schedule runs the script hourly at the 1st minute of every hour (ex. 6:01pm, 7:01pm, etc).
2. The script can be run without docker. Make sure to install pre-requisites from the Dockerfile and requirements.txt first and to schedule the script to run on a schedule using cron.
