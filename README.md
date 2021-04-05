# myturn-vaccine-find

This is a python3 script that can be run inside or outside of Docker on a cron schedule to scrape the myturn.ca.gov website for COVID-19 vaccination locations with potentially available appointment times. Notifications for potential sites with appointments will appear on the printed output in the command line terminal. There is also support for pushover.net's API for push notifications. NOTE: Pushover is a ~$5 purchase to unlock, but there may be a trial available.

## Required services
1. Pushover (this should be a one-time fee in the mobile phone app stores). Currently, appointment site matches are printed to the console. Pushover is used to send push notifications of these matches to a mobile device. Once purchased, export a user key and a token for use in the config.ini file within this repository.

## To download
1. Clone this repository into a working folder using 'git clone https://github.com/mgt20/myturn-vaccine-find.git'. Or, download using the GitHub WebGUI.

## To customize the script configuration
1. Rename config.sample.ini to config.ini
2. Modify Dockerfile with your timezone (make sure to use a supported Timezone syntax/variable).
3. Modify cronjobs file with your desired cron schedule. See crontab.guru for help with this.
4. Modify the config.ini file with your values for: pushover.net user and token. 
5. Modify config.ini file with your values for which location to search for on myturn.ca.gov. Use the location values from the last page of the tool exactly in this field.
6. IMPORTANT: The checkboxes/fields/questions are filled out automatically per my requirements. You can update these by Inspecting the webpage and copying the more relevant xpath or css selector for your answers and pasting them into the correct step in script.py. There are plans to make this customizable more easily in the script. For now, using the "Inspect" tool in your web browser and finding the correct identifier for the button/checkbox is required.

## To run on baremetal / without Docker
1. Install the required dependencies on your machine (see Dockerfile for OS packages needed and see requirements.txt for required pip packages).
2. Run the script by running: 'python3 script.py' while in the folder of the downloaded repository on your machine.

## To run on Docker
1. Have Docker and docker-compose installed and configured for use.
2. Run: 'docker-compose up --build" while in the working directory that houses the files downloaded from github to run the container. Optional: To run in "detached" mode instead (no print to console with process dependent on terminal window), instead run with -d flag added, such as: 'docker-compose up --build -d'

NOTES:
1. The current schedule runs the script hourly at the 1st minute of every hour (ex. 6:01pm, 7:01pm, etc).
