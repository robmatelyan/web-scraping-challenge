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
    mars_data = mongo.db.mars_data.find_one()
    #return data
    return render_template('index.html', mars_data=mars_data)

@app.route('/scrape')
def scrape():
    #create scrape function
    mars_data = scrape_mars.scrape()
    #update the db
    mongo.db.mars_data.update({}, mars_data, upsert=True)

    #redirect to home 
    return redirect('/', code=302)

if __name__ == '__main__':
    app.run(debug=True)