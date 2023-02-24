from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import requests
from bs4 import BeautifulSoup
import time
import os

"""THIS IS THE SCRIPT FOR SCRAPING WEBPAGES"""

def scrape_webpage(url):
    options = Options()
    options.add_argument('--headless')  # run the browser in headless mode
    options.add_argument('--disable-gpu')  # disable the GPU to save resources
    options.add_argument('--no-sandbox')  # disable the sandbox to avoid security issues

    driver = webdriver.Chrome(options=options)
    driver.get(url)

    time.sleep(5)  # wait for 5 seconds to let the page load completely

    html = driver.page_source

    url_parts_all = url.split('/')
    to_remove = ["https:", "", "www.classcentral.com", " "]
    url_parts = list(filter(lambda x: x not in to_remove, url_parts_all))
    dir = os.path.join(os.getcwd(), 'test_scrape')

    if len(url_parts) == 2:
        name = str(url_parts[1]) + ".html"
        dir_path = os.path.join(dir, url_parts[0])
        if not os.path.exists(dir_path):
            os.mkdir(os.path.join(dir, url_parts[0]))
        path = os.path.join(dir_path, name)

    elif len(url_parts) == 1:

        if len(url_parts[0]) >= 1:
            name = str(url_parts[0]) + ".html"
            path = os.path.join(dir, name)
        else:
            path = os.path.join(dir, 'index.html')

    with open(path, 'w', encoding='utf-8') as file:
        file.write(html)
        print(f"File {path} have been scraped!")


def links(site):
    urls = []
    
    agent = {"User-Agent":'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
    html = requests.get(site, headers=agent)

    
    # Parse the HTML content of the response using BeautifulSoup
    soup = BeautifulSoup(html.content, "lxml")
    

    for link in soup.find_all('a'):
        url = link.get('href')
        if url.startswith('/'):
            url = site + url[1:]
            
            if url not in urls:
                urls.append(url)

    return urls


if __name__ == "__main__":
    
    site = "https://www.classcentral.com/"
 
    urls = links(site)

    for i in urls:
        scrape_webpage(i)