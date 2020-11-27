#!/usr/bin/env python
# coding: utf-8

# # Scraping The Surface of Mars

# In[204]:


# Import Dependencies
import IPython
from IPython.display import display_html
from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
import pandas as pd


# In[8]:


# Mars URL page to be scraped for news title and paragraph text
site_news_url = 'https://mars.nasa.gov/news/'


# In[10]:


executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)

browser.visit(site_news_url)


# In[11]:


html = browser.html
soup = bs(html, 'html.parser')


# In[12]:


mars_subtags = soup.select_one('ul.item_list li.slide')


# In[13]:


# Latest News Title
news_title = mars_subtags.find('div', class_='content_title').get_text()
news_title


# In[14]:


# Paragraph Text
news_parag = mars_subtags.find('div', class_='article_teaser_body').get_text()
news_parag


# In[15]:


browser.quit()


# # Mars Featured Image

# In[38]:


# Mars URL page to be scraped for image
mars_site_image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'


# In[39]:


executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)

browser.visit(mars_site_image_url)


# In[40]:


browser.links.find_by_partial_text('FULL IMAGE').click()


# In[41]:


browser.links.find_by_partial_text('more info').click()


# In[43]:


# Get featured image
mars_featured_image_html = browser.html
mars_featured_image_soup = bs(mars_featured_image_html, 'html.parser')


# In[52]:


mars_featured_image_url = mars_featured_image_soup.select_one('figure.lede a')['href']
mars_featured_image_url


# In[53]:


large_image = 'https://www.jpl.nasa.gov' + mars_featured_image_url
print(large_image)
IPython.display.HTML('<img src=' + large_image + ' width=55%>')


# In[54]:


browser.quit()


# # Mars Facts

# In[73]:


# Assign Mars Facts webpage url to variant
mars_facts_url = 'https://space-facts.com/mars/'


# In[74]:


mars_facts_tables = pd.read_html(mars_facts_url)


# In[75]:


mars_facts_df = mars_facts_tables[0]
mars_facts_df.columns = ['Attributes', 'Data']


# In[76]:


# Display Mars Facts Dataframe
mars_facts_df.set_index('Attributes', inplace=True)
mars_facts_df


# In[77]:


# Convert the data to a HTML table string and save to file
mars_facts_df.to_html('mars_fact_table.html')


# In[88]:


# Convert dataframe to HTML string and display
mars_facts = mars_facts_df.to_html(header=True, index=True).replace('\n', '')
display_html(mars_facts, raw=True)


# # Mars Hemispheres

# In[149]:


# USGS Astrogeology site
astrogeoogy_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'


# In[150]:


# Initiate browser
executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)

browser.visit(astrogeoogy_url)


# In[151]:


# Create Empty Lists to Save image urls and Hemisphere titles
mars_hemisphere_image_urla = []
mars_hemisphere_image_urlb = []

mars_hemispheres = browser.find_by_css('a.product-item h3')
for hem in range(len(mars_hemispheres)):

    browser.find_by_css('a.product-item h3')[hem].click()
    
    sample_image = browser.links.find_by_text('Sample').first

# ---- dict a -----
    hemisphere_dicta = {
        'img_url' : sample_image['href'],
        'title' : browser.find_by_css('h2.title').text
    }
    
# ---- dict b -----
    hemisphere_dictb = {
        'Mars Hemisphere' : browser.find_by_css('h2.title').text.replace(' Hemisphere Enhanced',''),
        'URL' : sample_image['href']
    }
    
    mars_hemisphere_image_urla.append(hemisphere_dicta)
    mars_hemisphere_image_urlb.append(hemisphere_dictb)
    
    browser.back()

browser.quit()

pd.set_option('display.max_colwidth', None)

mars_hemisphere_df = pd.DataFrame.from_dict(mars_hemisphere_image_urlb)
mars_hemisphere_df.set_index('Mars Hemisphere', inplace=True)
display(mars_hemisphere_df)
print('-' * 42 + '  Mars Hemisphere Images  ' + '-' * 42)
display(mars_hemisphere_image_urla)


# In[230]:


image_a = IPython.display.HTML('<img src=' + mars_hemisphere_df['URL'][0] + ' width=25%>')
image_b = IPython.display.HTML('<img src=' + mars_hemisphere_df['URL'][1] + ' width=25%>')
image_c = IPython.display.HTML('<img src=' + mars_hemisphere_df['URL'][2] + ' width=25%>')
image_d = IPython.display.HTML('<img src=' + mars_hemisphere_df['URL'][3] + ' width=25%>')
display(image_a, image_b, image_c, image_d)


# In[ ]:




