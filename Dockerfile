# TODO 1. Specify the base image and its version (in this case, it's Python 3.10.4)
FROM python:3.10.4

# TODO 2. You can organize the working directory in the container using WORKDIR to set the working directory
WORKDIR /python-flask-server

# TODO 3. You can copy the requirements.txt into the working directory
COPY requirements.txt .

# TODO 4. You need to be able to install the requirements from the requirements.txt file
RUN pip3 install -r requirements.txt

# # TODO 5. Copy the main python script (in this case, it's main.py). This method is used for adding single files, folders or urls
# ADD main.py .

# TODO 6. Copy the folder containing the main python script (in this case we want to add the server folder)
COPY ./server /python-flask-server

# TODO 7. Expose the port that you want to use from the container side
EXPOSE 5000

# TODO 8. Define the FLASK_APP environment variable to define where your flask application is
ENV FLASK_APP="./app/main.py"

# TODO 9. Execute the main python script on container startup
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]

# TODO Next, we create a Docker Compose file, which we can use to handle multiple services (in our case, we want to run a web service (flask) and a db service(postgres))