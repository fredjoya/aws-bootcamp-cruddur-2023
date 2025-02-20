# Use an official Python runtime as a parent image
FROM python:3.10-slim-buster

# Set the working directory in the container
#make a new folder inside the container 
# (Inside Container)
WORKDIR /backend-flask

# Copy the current directory contents into the container at /usr/src/app 
# this contains the libraries want to install to run app
# (Outside Container -> Inside Container)
COPY requirements.txt requirements.txt 

# (Outside Container -> Inside Container)
# . means everything in the current directory 
# first . - means everything in the /backend-flask (outside container)
# second . - means everything in the /backend-flask (inside container)
COPY . . 

# Install any needed packages specified in requirements.txt
# intall the python libraries used for the app
# Inside Container
# python3 -m flask run --host=0.0.0.0 --port=4567 
RUN pip3 install -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 4567

# Define environment variable
# set environment variables {Env Vars}
# set Inside Container and will remain set when the container is running
ENV FLASK_ENV=development


# Run app.py when the container launches
# Command
CMD ["flask", "run", "--host=0.0.0.0", "--port=4567"]
