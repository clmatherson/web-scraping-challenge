from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo

from splinter import Browser
from bs4 import BeautifulSoup as bs

app = Flask(__name__)

app.config['MONGO_URI'] = 'mongodb://localhost:27017/marsscrape_db'
mongo = PyMongo(app)

@app.route('/')
def index():
    attribute = mongo.db.attributes.find_one()
    return render_template('index.html', attribute=attribute)

@app.route('/scrape')
def scrape():
    executable_path = {'executable_path': './chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)

    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)

    html = browser.html
    soup =bs(html, 'html.parser')

    try:
        title = soup.find('div', class_='content_title').text
    except:
        title = 'NASA News Title Not Available'
    
    try:
        paragraph = soup.find('div', class_='article_teaser_body').text
    except:
        paragraph = 'NASA News Paragraph Not Available'
    
    mars_site_image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(mars_site_image_url)

    browser.links.find_by_partial_text('FULL IMAGE').click()
    browser.links.find_by_partial_text('more info').click()
    browser.links.find_by_partial_href('/largesize/').click()

    mars_featured_image_html = browser.html
    mars_featured_image_soup = bs(mars_featured_image_html, 'html.parser')

    try:
        mars_featured_image_url = mars_featured_image_soup.select_one('img')['src']
    except:
        mars_featured_image_url = "NASA Image Not Available"

    image = mars_featured_image_url

    browser.quit()

    attribute = {
        'Title': title,
        'Paragraph': paragraph,
        'Image': image
    }

    mongo.db.attributes.update({}, attribute, upsert=True)

    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)