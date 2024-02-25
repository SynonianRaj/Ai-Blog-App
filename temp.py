url = "https://techcrunch.com/2024/02/21/google-launches-two-new-open-llms/"
import requests
from bs4 import BeautifulSoup

import requests
from bs4 import BeautifulSoup

# Specify the URL (replace with the actual URL)
# Fetch and parse the HTML content
res = requests.get(url)
res.raise_for_status()
soup = BeautifulSoup(res.content, 'html.parser')

# List of target texts to find in class names
target_texts = ["article__title", "article__byline", "image-credits","article-content","article__featured-image"]  # Replace with your actual list of texts

# Find all elements with any of the target texts in their class
matching_elements = soup.find_all(lambda tag: tag.has_attr('class') and any(text in tag['class'] for text in target_texts))

# Process the extracted elements
for element in matching_elements:
    # Access the element's text, attributes, or perform other actions
    element_text = element.text.strip()
    print(element_text)


    if matching_elements is not None:
        with open("index1.html", "w", encoding='utf8') as file:
            file.write(str(matching_elements))

        print("Body tag with script tags removed and saved to index1.html")
    else:
        print("Body tag not found in the HTML content.")


