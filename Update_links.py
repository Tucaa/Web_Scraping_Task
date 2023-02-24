import os
from bs4 import BeautifulSoup

"""THIS IS THE SCRIPT FOR UPDATTING LINKS IN INDEX(HOME) HTML FFILE IN ORDER TO LINK ALL SCRAPED PAGES TO IT"""

def add_html_to_links(html):
    
    soup = BeautifulSoup(html, 'html.parser')
    for link in soup.find_all('a'):
        href = link.get('href')
        if href and not href.endswith('.html'):
            link['href'] = href + '.html'

    return str(soup)


if __name__ == "__main__":

    file_path = input("Enter absolute path of file: ")

    with open(file_path, 'r', encoding='utf-8') as f:
        html = f.read()

        modified_html = add_html_to_links(html)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(modified_html)
        print(f"Links in file {os.path.basename(file_path)} have been updated")

