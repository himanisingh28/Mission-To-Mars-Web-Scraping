# Dependencies
from bs4 import BeautifulSoup
import requests
from splinter import Browser
import pandas as pd
import time

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {'executable_path': r'C:/Users/HimaniAkshay/chromedriver_win32/chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)

# Create dictionary that can be imported into Mongo
mars_data = {}

def scrape():
    browser = init_browser()

    #NASA Mars News
    # URL of NASA Mars News page to be scraped
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    time.sleep(5)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    # results returned 
    tresult = soup.find('div', class_="content_title")
    news_title = tresult.find('a').text
    presults = soup.find('div', class_="article_teaser_body")
    news_p = presults.text


    # URL for JPL Featured Space image page to be scraped
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    base_url = 'https://www.jpl.nasa.gov'
    browser.visit(url)
    time.sleep(1)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    li_result = soup.find('li', class_='slide')

    fb_result = li_result.find('a', class_='fancybox')

    url_result = fb_result.get('data-fancybox-href')
    featured_image_url = base_url + url_result
    

    #URL for Mars Weather Twitter account
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    div_result = soup.find('div', class_= 'js-tweet-text-container')
    mars_weather = div_result.find('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text').text


    #URL for Mars Facts
    url = 'https://space-facts.com/mars/'
    tables = pd.read_html(url)

    mars_data_df = tables[0]

    mars_data_df.columns = ['Parameters', 'Value']
    mars_data_df.set_index('Parameters', inplace=True)
    mars_html_table = mars_data_df.to_html()

    #Mars Hemispheres
    #Url for USGS astrogeology site
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    hemisphere_image_urls = []
    hemi_dict = {}
    partial_url = 'https://astrogeology.usgs.gov'

    item_results = soup.findAll('div', class_='item')

    for each in item_results:
        img_link = each.find('a', class_='itemLink product-item')['href']
        complete_url = partial_url + img_link
    
        browser.visit(complete_url)
        html = browser.html
        bsoup = BeautifulSoup(html, 'html.parser')
    
        image_results = bsoup.find('img', class_='wide-image')['src']
        img_url = partial_url+image_results
        title_results = bsoup.find('h2', class_= 'title').text.strip('Enhanced')
    
    
        hemi_dict = {"title": title_results, "img_url": img_url}
        hemisphere_image_urls.append(hemi_dict)

    #Store Mars data in a dictionary
    mars_data = { "news_title": news_title,
                    "news_content": news_p,
                    "featured_image_url": featured_image_url,
                    "mars_weather": mars_weather,
                    "mars_html_table": mars_html_table,
                    "hemisphere_image_urls": hemisphere_image_urls}

    # Quite the browser after scraping
    browser.quit()

    # Return news data dictionary
    return mars_data