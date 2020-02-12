# this is an official Python runtime, used as the parent image
FROM python:3.6.5-slim

ENV http_proxy  16.167.28.210:8080
ENV https_proxy  16.167.28.210:8080

# set the working directory in the container to /app
WORKDIR /app

# add the current directory to the container as /app
ADD . /app

# execute everyone's favorite pip command, pip install -r
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# unblock port 80 for the Bottle app to run on
EXPOSE 80

# execute the Bottle app
CMD ["python", "myapp.py"]