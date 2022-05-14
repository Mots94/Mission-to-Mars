from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

executable_path = {'executable_path': ChromeDriverManager().install()}

browser = Browser('chrome', **executable_path, headless=False)

# Assign the url to visit
url = 'https://redplanetscience.com'

browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)

html = browser.html

news_soup = soup(html, 'html.parser')

slide_elem = news_soup.select_one('div.list_text')

slide_elem.find('div', class_='content_title')

news_title = slide_elem.find('div', class_='content_title').get_text()

news_title

news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

news_p


# ### Featured Images

# Visit Space images url

url = 'https://spaceimages-mars.com/'

browser.visit(url)

full_image_elem = browser.find_by_tag('button')[1]

full_image_elem.click()

html = browser.html

img_soup = soup(html, 'html.parser')

# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

img_url_rel

img_url = f'https://spaceimages-mars.com/{img_url_rel}'

img_url

# Pull Mars facts for app.

df = pd.read_html('https://galaxyfacts-mars.com/')[0]

df.columns=['description', 'Mars', 'Earth']

df.set_index('description', inplace=True)

df

df.to_html()



# Use an automated browser to visit Mars Hemispheres webpage

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

    link.click()

    # Initialize html parser

    html = browser.html

    # Create bs object

    bs = soup(html, 'html.parser')

    # Parse html and find .jpg image link and title

    downloads = bs.find('div', class_='downloads')
    hem_img = downloads.find('a').get('href')

    title = bs.find('h2', class_='title').text

    # Add .jpg link and title to dictionary

    hemispheres = {
        'img_url':hem_img,
        'title':title 
    }

    # Append list with each dictionary created

    hems_image_urls.append(hemispheres)

    browser.back()

browser.quit()