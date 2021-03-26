from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# flask setup
app = Flask(__name__)

# create mongodb connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

@app.route('/')
def index():
    #find one record from db
    mars_dict = mongo.db.collection.find_one()
    #return data
    return render_template('index.html', mars_info=mars_dict)

@app.route('/scrape')
def scrape():
    #create scrape function
    mars_info = scarpe_mars.scrape()
    #update the db
    mongo.db.collection.update({}, mars_info, upsert=True)

    #redirect to home 
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)