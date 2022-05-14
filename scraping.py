from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt
import time

def scrape_all():

    # Initiate headless driver for deployment

    executable_path = {'executable_path': ChromeDriverManager().install()}

    browser = Browser('chrome', **executable_path, headless=False)

    # Mars news function will be used to pull this data
    
    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in a dictionary

    data = {

        'news_title': news_title,

        'news_paragraph': news_paragraph,

        'featured_image': feat_img(browser),

        'facts': mars_facts(),

        'hemispheres': hem_images(browser),

        'last_modified': dt.datetime.now()
    }

    browser.quit()

    return data

def mars_news(browser):

    # Assign the url to visit
    url = 'https://redplanetscience.com'

    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object

    html = browser.html

    news_soup = soup(html, 'html.parser')

    try:

        slide_elem = news_soup.select_one('div.list_text')

        # Use the parent element to find the first 'a' tag and save is as 'news_title'

        news_title = slide_elem.find('div', class_='content_title').get_text()

        # Use the parent element to find the paragraph text

        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    except AttributeError:

        return None, None

    return news_title, news_p

### Featured Images

# Visit Space images url

def feat_img(browser):

    # Visit the url

    url = 'https://spaceimages-mars.com/'

    browser.visit(url)

    # Find and clikc the full image button

    full_image_elem = browser.find_by_tag('button')[1]

    full_image_elem.click()

    # Parse the resulting html with soup

    html = browser.html

    img_soup = soup(html, 'html.parser')

    # Use try/except for error handling

    try:
    
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:

        return None

    # Use base url to create an absolute url

    img_url = f'https://spaceimages-mars.com/{img_url_rel}'

    return img_url

def mars_facts():

    try:

        # Use 'read_html' to scrape the facts table into a dataframe

        df = pd.read_html('https://galaxyfacts-mars.com/')[0]

    except BaseException:

        return None

    df.columns=['Description', 'Mars', 'Earth']

    df.set_index('Description', inplace=True)

    return df.to_html()

def hem_images(browser):

    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    browser.visit(url)


    # Create lists for .jpg hemisphere images and titles

    hems_image_urls = []

    # Retreive full resolution hemisphere images and titles

    image_pages = browser.find_by_tag('h3')

    # Loop through starting links

    for link in image_pages:

        # Empty dictionary for key values pairs (link & title)

        hemispheres = {}

        # Click the link to visit specific hemisphere page
        time.sleep(1)
        
        link.click()

        # Initialize html parser

        html = browser.html

        # Create bs object

        bs = soup(html, 'html.parser')

        try:

            # Parse html and find .jpg image link and title

            downloads = bs.find('div', class_='downloads')
            hem_img = downloads.find('a').get('href')

            title = bs.find('h2', class_='title').text

        except AttributeError:

            return None

        # Add .jpg link and title to dictionary

        hemispheres = {
            'img_url':hem_img,
            'title':title 
        }

        # Append list with each dictionary created

        hems_image_urls.append(hemispheres)

        browser.back()


    return hems_image_urls

if __name__ == '__main__':

    # If running as script, print scraped data

    print(scrape_all())