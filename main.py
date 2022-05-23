# Goal: Create an API that fetches the top 10 repositories from the GitHub API and writes them to a PostgreSQL database

from flask import Flask
from flask_restful import Api, Resource
import requests

app = Flask(__name__)
api = Api(app)

# Define a list to store response
response = requests.get("https://api.github.com/search/repositories?q=stars:>0&sort=stars&order=desc&page=1&per_page=10").json()
top10 = response["items"]

# Create a resource
class Repository(Resource):
    # GET method
    def get(self):
        return top10

# Add the resource to the API under an appropriate route
api.add_resource(Repository, "/repos/top10")

# Run the server in debug mode
if __name__ == "__main__":
    app.run(debug=True)