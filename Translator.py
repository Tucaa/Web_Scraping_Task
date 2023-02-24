from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup
from googletrans import Translator
import os
import httpx

"""THIS IS THE SCRIPT FOR TRANSLATION OFF ALL DISPLAYED TEXT IN .HTML FILE. IT USES GOOGLE TRANSLATE API"""

def translate(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        html_doc = f.read()

    # Parse the HTML document with Beautiful Soup
    soup = BeautifulSoup(html_doc, 'html.parser')

    visible_text_elements = soup.find_all(string=True)

    # Use a ThreadPoolExecutor to parallelize the translation process
    with ThreadPoolExecutor() as executor:
        future_to_element = {}
        for element in visible_text_elements:
            if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
                # Skip over any non-text elements
                continue
            visible_text = str(element).strip()
            if visible_text:
                future = executor.submit(translate_text, visible_text)
                future_to_element[future] = element

        # Replace the translated text in the soup as the futures complete
        for future in future_to_element:
            element = future_to_element[future]
            translated_text = future.result()
            element.replace_with(translated_text)

    # Write the translated HTML to the input file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(str(soup))
        print(f"File {file_path} has been translated to hindi!")

def translate_text(text):
    translator = Translator(timeout=httpx.Timeout(30))
    return translator.translate(text, dest='hi').text



def get_file_paths(directory):
    file_paths = []

    # Iterate over all the files and directories in the directory
    for root, directories, files in os.walk(directory):
        # Iterate over all the files in the directory
        for filename in files:
            # Get the full path of the file
            path = os.path.join(root, filename)

            # Add the file path to the list
            file_paths.append(path)

    return file_paths


if __name__ == "__main__":

    dir = input("Enter path of directory: ")
    paths = get_file_paths(dir)

    for path in paths:
            translate(path)
    