#  get python
FROM python:3.7-slim

# set working directory to /app
WORKDIR /app

# copy current directory to container at /app
COPY . /app

# install gcc
RUN apt-get update -y 
RUN apt-get install  -y --no-install-recommends gcc
RUN apt-get install -y libc-dev

# install packages
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# make port 80 avaiable 
EXPOSE 80


# run app.py inside container on launch
CMD ["python", "app.py"]