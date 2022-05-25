# Goal: Create an API that fetches the top 10 repositories from the GitHub API and writes them to a PostgreSQL database

from flask import Flask
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import requests

# docker exec -it github-top-10-repos_db_1 bash
# psql -h 0.0.0.0 -p 5432 -U postgres

app = Flask(__name__)
api = Api(app)

# Define the SQLAcademy URI and configure a database and its engine
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg2://postgres:admin@db:5432/repos"
db = SQLAlchemy(app)
engine = db.engine

# Migrate to DB
migrate = Migrate(app, db)

# Create a database model for storing responses
class Repository(db.Model):
    __tablename__ = "top10repos"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))
    stars = db.Column(db.Integer)

    def __init__(self, id, name, stars):
        self.id = id
        self.name = name
        self.stars = stars


# Define a list to store the response from GitHub API
response = requests.get("https://api.github.com/search/repositories?q=stars:>0&sort=stars&order=desc&page=1&per_page=10").json()
top10repos = []

# Each item is appended to the list
for item in enumerate(response["items"]):
    top10repos.append({"id": item["id"], "name": item["name"], "stars": item["stargazers_count"]})

# If the table does not exist, we create it
if not engine.dialect.has_table(engine, Repository.__tablename__):
    Repository.__table__.create(engine)

# Clear the table
db.session.query(Repository).delete()
db.session.commit()

# Add each item to the database
for item in top10repos:
    repo = Repository(item["id"], item["name"], item["stars"])
    db.session.add(repo)
    db.session.commit()

# Create a resource
class Repositories(Resource):
    # GET method
    def get(self):
        return Repository.query.all()

# Add the resource to the API under an appropriate route
api.add_resource(Repositories, "/repos/top10")

# Run the server in debug mode
if __name__ == "__main__":
    app.run(port=5500, host="0.0.0.0")