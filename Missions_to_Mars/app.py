# import necessary libraries

from flask import Flask, redirect, render_template
import scrape_mars
from flask_pymongo import PyMongo

# create instance of Flask app
app = Flask(__name__)

mongo = PyMongo(app, uri='mongodb://localhost:27017/missionToMars_DB')


@app.route("/scrape")
def scrape():
    scraped_mars_data = scrape_mars.scrape()

    mongo.db.marsNews.update_one({}, {"$set": scraped_mars_data}, upsert=True)


    return redirect("/")



@app.route("/")
def home():
    mars_data = mongo.db.marsNews.find_one()

    print(list(mars_data))

    return render_template("index.html", mars = mars_data)





if __name__ == "__main__":
    app.run(debug=True)
