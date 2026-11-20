from database import createTables
from flask import Flask

app = Flask(__name__)
@app.route('/')
def home():
    return "This is Home Page.."

if __name__ == "__main__":
    print(createTables())
    app.run(debug=True)