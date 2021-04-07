FROM python:3.9.3-slim-buster

RUN apt-get update && apt-get install -yq \
    chromium=89.0.4389.114-1~deb10u1 \  
    chromium-driver=89.0.4389.114-1~deb10u1 \
    python3-selenium=3.14.1+dfsg1-1 \
    cron=3.0pl1-134+deb10u1

RUN mkdir app

WORKDIR /app 

# Set pythonpath to the working directory of the container
ENV PYTHONPATH "${PYTHONPATH}:/app"

# create symlinks to chromedriver and geckodriver (to the PATH)
RUN chmod 777 /usr/bin/chromedriver

# Copy required files into the working directory of the container
COPY script.py script.py
COPY requirements.txt requirements.txt
COPY cronjobs /etc/cron.d/cronjobs
COPY config.ini config.ini

# Install pip requirements into container
RUN pip3 install -r requirements.txt

# Set permissions for the cronjobs file
RUN chmod 644 /etc/cron.d/cronjobs

# Run cron after boot
CMD ["cron", "-f"]

