# import modules
from splinter import Browser
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup as bs
import pandas as pd
import pymongo
import time
import requests

def scrape():
    

    # Setup splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # visit url
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)
    html = browser.html
    time.sleep(2)
    soup = bs(html, 'html.parser')

    # NASA Mars News
    nasa_article = soup.find_all('li', class_='slide')
    print(nasa_article[0])

    # retrieve the title
    news_title = nasa_article[0].find('div', class_='content_title').text
    news_title

    # retrieve most recent article teaser
    news_p = nasa_article[0].find('div', class_='article_teaser_body').text
    news_p

    # JPL Mars Space Images - Featured Image
    jpl_url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(jpl_url)
    html = browser.html
    time.sleep(2)
    soup = bs(html, 'html.parser')
    image = soup.find_all('img', class_='headerimage fade-in')[0]['src']
    image 

    jpl_url_base = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/'
    featured_image_url = jpl_url_base + image
    featured_image_url

    # Mars Facts
    mars_facts_url = 'https://space-facts.com/mars/'

    # read table
    tables = pd.read_html(mars_facts_url)
    tables

    mars_df = tables[0]
    mars_df

    # drop all single header rows
    mars_df.columns = ['', 'Mars']
    mars_df

    #convert to HTML

    html_table = mars_df.to_html()
    html_table

    # strip unwanted new lines 
    html_table.replace('\n', '')

    # save html
    mars_df.to_html('table.html')

    # Mars Hemispheres
    hemisphere_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    browser.visit(hemisphere_url)
    html = browser.html
    time.sleep(2)
    soup = bs(html, 'html.parser')
    hemisphere_names = soup.find_all(class_='description')

    # create name list 
    name_list = []

    # for loop to retrieve names
    for name in hemisphere_names:
        name_list.append(name.a.h3.text)
    name_list

    #retireve images
    browser.visit(hemisphere_url)

    #create list for urls
    hemisphere_images = []

    # for loop to retrieve images
    for i in range(len(name_list)):
        browser.click_link_by_partial_text(name_list[i])
        html = browser.html
        soup = bs(html, 'html.parser')
        title = name_list[i]
        img_url = soup.find(class_='downloads')
        hemisphere_dict = {}
        hemisphere_dict['title'] = title
        hemisphere_dict['img_url{0}'] = img_url.a['href']
        hemisphere_images.append(hemisphere_dict)
        browser.back()
    hemisphere_images

    # quit browser

    browser.quit()

    mars_dict = {
        'news_title': news_title,
        'news_p': news_p,
        'featured_image_url': featured_image_url,
        'mars_table': html_table,
        'hemisphere_image_urls': hemisphere_images
    }

    return mars_dict