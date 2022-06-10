from bs4 import BeautifulSoup as bs

import requests as r
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from splinter import Browser
import time

def scrape():
    # Setup splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    time.sleep(10)
    

    newsURL = 'https://redplanetscience.com/'
    browser.visit(newsURL)
    time.sleep(5)
    newsHtml = browser.html
    time.sleep(5)
    soup1 = bs(newsHtml, 'html.parser')

    

    title_result = soup1.find("div", class_='content_title')
    news_title = title_result.text
    #print(news_title)

    paragraph_result = soup1.find("div", class_='article_teaser_body')
    news_p = paragraph_result.text
    #print(news_p)

    newsData = [news_title, news_p]


    #####
    jplURL = 'https://spaceimages-mars.com/'
    browser.visit(jplURL)
    jpl_html = browser.html
    soup2 = bs(jpl_html, 'html.parser')
    featured_image_url = browser.links.find_by_partial_href('jpg').first['href']



    #####
    mars_facts_url = 'https://galaxyfacts-mars.com/'

    tables = pd.read_html(mars_facts_url)


    mars_v_earth_df = tables[0]
    mars_facts_df = tables[1]


    mars_v_earth_df = mars_v_earth_df.rename(columns={0:"",1:"Mars",2:"Earth"}).drop([0])


    mars_v_earth_df.reset_index(inplace=True, drop=True)


    html_table = mars_v_earth_df.to_html()


    html_table = html_table.replace('\n', '')


    #####


    hemisphere_image_urls = [
        {"title": "Valles Marineris Hemisphere", "img_url": "https://marshemispheres.com/images/b3c7c6c9138f57b4756be9b9c43e3a48_valles_marineris_enhanced.tif_full.jpg"},
        {"title": "Cerberus Hemisphere", "img_url": "https://marshemispheres.com/images/f5e372a36edfa389625da6d0cc25d905_cerberus_enhanced.tif_full.jpg"},
        {"title": "Schiaparelli Hemisphere", "img_url": "https://marshemispheres.com/images/3778f7b43bbbc89d6e3cfabb3613ba93_schiaparelli_enhanced.tif_full.jpg"},
        {"title": "Syrtis Major Hemisphere", "img_url": "https://marshemispheres.com/images/555e6403a6ddd7ba16ddb0e471cadcf7_syrtis_major_enhanced.tif_full.jpg"},
    ]


    mars_data = {
        "news": newsData,
        "featured": featured_image_url,
        "table": html_table,
        "images": hemisphere_image_urls

    }


    browser.quit()

    return mars_data


