## Introduction to Flask for creating RESTful APIs ##

# Goal: Create a Dockerized API that fetches the top 10 repositories from the GitHub API and writes them to a PostgreSQL database

# Important! You need to create a virtual environment to install Flask.
# To create a virtual environment, go to Terminal, cd to project directory then type "python3 -m venv .venv" and "source .venv/bin/activate"

# You also need a requirements.txt file like the one in this project's directory to install Flask
# To install requirements, go to Terminal, cd to project directory then type "pip3 install -r requirements.txt"

# TODO 1. Import statements
from flask import Flask
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import requests

# TODO 2. Define app and API
app = Flask(__name__)
api = Api(app)

# TODO 9. Define the SQLAcademy URI and configure a database and its engine
# The URI should be in the format "postgresql+psycopg2://username:password@db_container_name:port/db_name"
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg2://postgres:admin@db:5432/repos"
db = SQLAlchemy(app)
engine = db.engine

# TODO 10. Define a migration to the database
migrate = Migrate(app, db)

# TODO 11. Create a database model for storing responses
class Repository(db.Model):
    __tablename__ = "top10repos"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))
    stars = db.Column(db.Integer)

    def __init__(self, name, stars):
        self.name = name
        self.stars = stars

# TODO 7. Query GitHub API to get the top 10 repositories sorted in descending order by the number of stars
response = requests.get("https://api.github.com/search/repositories?q=stars:>0&sort=stars&order=desc&page=1&per_page=10").json()

# TODO 8. Create a list to temporarily store the results
top10repos = []
for index, item in enumerate(response["items"]):
    top10repos.append({"name": item["name"], "stars": item["stargazers_count"]})

# TODO 12. Add the top 10 repos from the list to the database
# Check if the table exists. If it does not exist, create it
if not engine.dialect.has_table(engine, Repository.__tablename__):
    Repository.__table__.create(engine)

# Clear the table to insert the new values
db.session.query(Repository).delete()
db.session.commit()

# Add each item from the list to the database
for item in top10repos:
    repo = Repository(item["name"], item["stars"])
    db.session.add(repo)
    db.session.commit()

# TODO 13. Create a function to parse a query result row to a dictionary with the columns as keys and row values as values
def rowToDict(row):
    d = {}
    for column in row.__table__.columns:
        d[column.name] = str(getattr(row, column.name))
    return d

# TODO 4. Create a resource
class Repositories(Resource):
    # TODO 5. Add methods to handle different kinds of HTTP requests
    # Handling a GET request sent to the resource URL
    def get(self):
        # Get all the data in the top10repos table
        query = db.session.query(Repository).all()
        # Convert each item to a dictionary
        for index, row in enumerate(query):
            query[index] = rowToDict(row)
        # Return the result as a list of dictionaries
        return query

# TODO 6. Add the resource to the API under an appropriate route
api.add_resource(Repositories, "/repos/top10")

# TODO 3. Run the server in debug mode
if __name__ == "__main__":
    # Define host and port (if dockerized, use host 0.0.0.0 with whichever port you exposed in the Dockerfile)
    app.run(port=5000, host="0.0.0.0")

# TODO Next, we create a Dockerfile and Docker Compose file (move to Dockerfile)