import feedparser
from datetime import datetime
import requests
from bs4 import BeautifulSoup


def fetch_and_sort_articles(feed_url):
   """Fetches articles from an RSS feed, sorts them by publication date, and returns a sorted list of article dictionaries.

   Args:
       feed_url (str): The URL of the RSS feed to fetch.

   Returns:
       list: A list of article dictionaries, sorted by publication date in descending order.
   """

   feed = feedparser.parse(feed_url)
   articles = []

   for entry in feed.entries:
       try:
           pubDate = datetime.strptime(entry.published, "%a, %d %b %Y %H:%M:%S %z")  # Parse date efficiently
       except ValueError:
           # Handle cases where publication date is missing or invalid
           pubDate = None

       article = {
           "title": entry.title,
           "link": entry.link,
           "description": entry.description,
           "pubDate": pubDate,
           "author": entry.author,
       }

       articles.append(article)

   articles.sort(key=lambda article: article["pubDate"], reverse=True)
   return articles

# Example usage:
articles = fetch_and_sort_articles("https://techcrunch.com/feed/")

def scrape_content(url):
   res = requests.get(url)
   res.raise_for_status()
   soup = BeautifulSoup(res.content, 'html.parser')

   # List of target texts to find in class names
   target_texts = ["article__title", "article__byline", "image-credits","article-content","article__featured-image" ]  # Replace with your actual list of texts

   return soup.find_all(lambda tag: tag.has_attr('class') and any(
       text in tag['class'] for text in target_texts))

print("completed-utills")
