from flask import Flask 
#create a Flask application instance
app = Flask(__name__) 
#__name__ is saying its a Flask object
#now we will start defining the routes
@app.route('/')
def home():
    """Default home page"""
    return "Hello PFS-VSP-004 guys keep going"
@app.route('/saketh')
def details():
    """Details aboout Saketh"""
    return "Saketh is Co-Founder of Codegnan and good"
@app.route('/students')
def data():
    """Students info"""
    return "Students are from Codegnan"
if __name__ == "__main__":
    #if port is already in use change the port numbers
    app.run(host='0.0.0.0',
            port=5500,debug=True)