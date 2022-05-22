# Goal: Create an API that fetches the top 10 repositories from the GitHub API and writes them to a PostgreSQL database

from flask import Flask
from flask_restful import Api, Resource
import requests

app = Flask(__name__)
api = Api(app)

# Define a list to store responses
response = requests.get("https://api.github.com/search/repositories?q=stars:>0&sort=stars&order=desc&perpage=10/1").json()
repositories = response["items"]
top10 = repositories[:10]

# Create a resource
class Repository(Resource):
    # GET method
    def get(self):
        return top10
    
# Add the resource to the API under a URL
api.add_resource(Repository, "/top10")


# Run the server in debug mode
if __name__ == "__main__":
    app.run(debug=True)
