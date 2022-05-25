FROM python:3.10.4
WORKDIR /python-flask-server
COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY ./server /python-flask-server
EXPOSE 5000
ENV FLASK_APP="./app/main.py"
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]