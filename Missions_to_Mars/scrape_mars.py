#!/usr/bin/env python
# coding: utf-8

# # Scraping The Surface of Mars

# In[178]:


# Import Dependencies
import os
import IPython
from IPython.display import display_html
from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
from PIL import Image  
import PIL
import pandas as pd

from flask import Flask, render_template, session, redirect
from flask_pymongo import PyMongo

import time

app = Flask(__name__)

app.config['MONGO_URI'] = 'mongodb://localhost:27017/marsscrape_db'
mongo = PyMongo(app)

# In[179]:
def mars_news(browser):
    
# Mars URL page to be scraped for news title and paragraph text
    site_news_url = 'https://mars.nasa.gov/news/'


# In[180]:


    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    browser.visit(site_news_url)
    time.sleep(5)

# In[181]:
# News Title
    newstitle_attempts = 0

    while newstitle_attempts < 5:
        try:
            html = browser.html
            soup = bs(html, 'html.parser')
            mars_subtags = soup.select_one("ul.item_list li.slide")

            news_title = mars_subtags.find("div", class_="content_title").get_text()
            break
        except:
            newstitle_attempts +=1
            time.sleep(5)
            if newstitle_attempts >= 5:
                news_title = "NASA News Title Not Availble"

# In[184]:

# Paragraph Text
    paratext_attempts = 0

    while paratext_attempts < 5:
        try:
            html = browser.html
            soup = bs(html, 'html.parser')
            mars_subtags = soup.select_one("ul.item_list li.slide")

            news_parag = mars_subtags.find('div', class_='article_teaser_body').get_text()
            break
        except:
            paratext_attempts +=1
            time.sleep(5)
            if paratext_attempts >=5:
                news_parag = "NASA Paragraph Text Not Available"


# In[185]:

    browser.quit()

    return news_title, news_parag

# In[186]:

def featured_image(browser):
# Mars URL page to be scraped for image
    mars_site_image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'

# In[187]:
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

# Navagate with Browser to Largesize Image
    browser.visit(mars_site_image_url)
    browser.links.find_by_partial_text('FULL IMAGE').click()
    browser.links.find_by_partial_text('more info').click()
    browser.links.find_by_partial_href('/largesize/').click()

# Get featured image
    mars_featured_image_html = browser.html
    mars_featured_image_soup = bs(mars_featured_image_html, 'html.parser')

    mars_featured_image_url = mars_featured_image_soup.select_one('img')['src']
    
    browser.quit()

    return mars_featured_image_url

# In[189]:

def mars_facts(browser):
# Assign Mars Facts webpage url to variant
    mars_facts_url = 'https://space-facts.com/mars/'


# In[190]:
    mars_facts_tables = pd.read_html(mars_facts_url)

# In[191]:
    mars_facts_df = mars_facts_tables[0]
    mars_facts_df.columns = ['Attributes', 'Data']

# In[192]:
# Display Mars Facts Dataframe
    mars_facts_df.set_index('Attributes', inplace=True)
    # mars_facts_df

    mars_table = mars_facts_df.to_html(classes="table table-striped")

# In[193]:
    browser.quit()

# Convert the data to a HTML table string and save to file
    return mars_table

# In[194]:
# # Mars Hemispheres

# In[195]:
def hemisphere(browser):
    
# USGS Astrogeology site
    astrogeoogy_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

# In[196]:
# Initiate browser
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    browser.visit(astrogeoogy_url)

# In[197]:
# Create Empty Lists to Save image urls and Hemisphere titles
    mars_hemisphere_image_urla = []

    mars_hemispheres = browser.find_by_css('a.product-item h3')
    for hem in range(len(mars_hemispheres)):

        browser.find_by_css('a.product-item h3')[hem].click()
    
        sample_image = browser.links.find_by_text('Sample').first

# ---- dict a -----
        hemisphere_dicta = {
            'img_url' : sample_image['href'],
            'title' : browser.find_by_css('h2.title').text
        }

        mars_hemisphere_image_urla.append(hemisphere_dicta)
    
        browser.back()
    
    browser.quit()
    
    return mars_hemisphere_image_urla
    
# In[ ]:
@app.route('/')
def index():
    attribute = mongo.db.attributes.find_one()
    return render_template('index.html', attribute=attribute)

@app.route('/scrape')
def scrape():
    executable_path = {'executable_path': './chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)

    news_title, news_parag = mars_news(browser)
    img_url = featured_image(browser)
    mars_table = mars_facts(browser)
    mars_hemisphere_image_urla = hemisphere(browser)

    attribute = {
        "news_title": news_title,
        "news_paragraph": news_parag,
        "feature_image": img_url,
        "facts": mars_table,
        "hemispheres": mars_hemisphere_image_urla
        }

    mongo.db.attributes.update({}, attribute, upsert=True)

    browser.quit()

    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)

