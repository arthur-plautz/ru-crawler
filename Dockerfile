FROM python:3.7

# install google chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get -y update
RUN apt-get install -y google-chrome-stable

# install chromedriver
RUN apt-get install -yqq unzip
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

# set chromedriver as driver
ENV DRIVER=chromedriver

# set display port to avoid crash
ENV DISPLAY=:99

RUN cd | mkdir scraper

COPY ./requirements.txt ./scraper/requirements.txt
COPY ./src/models ./scraper/src/models/
COPY ./src/scripts ./scraper/src/scripts/

RUN pip install -r ./scraper/requirements.txt

COPY ./entrypoint.sh ./entrypoint.sh

RUN chmod +x ./entrypoint.sh

ENTRYPOINT [ "bash", "./entrypoint.sh" ]