import os
from bs4 import BeautifulSoup
import re

"""THIS IS FILE FOR CORRECTION OFF THE LINKS ITS NEEDED BECAUSE SOME LINKS HAVE DIFFERENT FORMAT. BECAUSE OF THAT SOME LINKS DID NOT WORK IN THE FIRST PLACE
TO USE THIS FILE YOU NEED TO INPUT ABSOLUTE PATH OF .HTML FILE """


def add_html_to_links(html):
    
    soup = BeautifulSoup(html, 'html.parser')
    for link in soup.find_all('a'):
        href = link.get('href')
        if href.startswith('https://www.classcentral.com/'):
            new_href = re.sub(r'^https://www\.classcentral\.com', '', href)
            link['href'] = new_href
            if href.endswith('/.html'):
                link['href'] = href[:-6] + '.html'
    
        # check if string ends with '/ .html'
            if href.endswith('/ .html'):
                link['href'] = href[:-7] + '.html'

    return str(soup)


if __name__ == "__main__":

    file_path = input("Enter absolute path of file: ")

    with open(file_path, 'r', encoding='utf-8') as f:
        html = f.read()

        modified_html = add_html_to_links(html)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(modified_html)
        print(f"Links in file {os.path.basename(file_path)} have been updated")