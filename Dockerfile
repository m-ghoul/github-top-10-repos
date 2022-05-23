FROM python:3.10.4
WORKDIR /python-flask-server
COPY requirements.txt .
COPY ./server ./server
RUN pip3 install -r requirements.txt
EXPOSE 5000
ENV FLASK_APP="./server/main.py"
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]