#pip install flask

import flask
from flask import Flask

#We will initialize the Flask application instance
app = Flask(__name__)

#now we will define a route for the url
@app.route('/')
def home():
    return "PFS-VSP-OO4 Students are good but need more concentration"

if __name__ == "__main__":
    #run the local development server
    app.run()
