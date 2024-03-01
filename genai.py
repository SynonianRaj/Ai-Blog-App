
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "adminApp.settings")
import django
django.setup()

import google.generativeai as genai
from blog.utils import scrape_content, fetch_and_sort_articles
import re ,json

from blog.models import Posts
from api_keys import API_KEY
# configure Gemini API key here
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-pro')



def clean(data):
    # pattern = r"^{[\s\S]*?}$\s.*\s}$"  # Matches text within curly braces
    pattern = r"{[\s\S]*}*}"
    matches = re.search(pattern, data, re.MULTILINE)
    i,e = matches.span()

    return data[i:e]

prompt = """
    extract the title,meta and images and return in json format from the given html-
    **Title:** Please identify the existing title and rewrite it as a more engaging and concise one.
    **author:** Please add author name.
    **author_profile_link:** Identify author profile link and add here.
    **Meta:** Please add author name and his profile link and relevant meta keywords.
    **keywords:** Generate comma seperated list of SEO optimized keywords based on give html above.

    **Images:** Please leave any existing <img> tags intact.
    **Images_alt_text:** Re-write Image alt text.
    **Image_credits:** Identify Image owner name and add here.

    for example as below -
    {
    "title": "Introducing Gemma: Google's New Open LLMs for Versatile AI Applications",
    "author": "Frederic Lardinois",
    "author_profile_link": "https://techcrunch.com/author/frederic-lardinois/",
    "meta": [
    "Gemma Open LLMs",
    "Google AI",
    "Natural Language Processing",
    "Machine Learning",
    "AI Development",
    "Frederic Lardinois"
    ],
    "keywords": [
    "Gemma",
    "Google",
    "Open LLMs",
    "Artificial Intelligence",
    "Natural Language Processing",
    "Machine Learning",
    "AI Applications",
    "AI Development"
    ],
    "images": [
    {
    "src": "https://techcrunch.com/wp-content/uploads/2024/02/GettyImages-1279291007.jpg?w=481",
    "alt": "Gemma, Google's New Open LLMs for Versatile AI Applications"
    }
    ],
    }
    """



articles = fetch_and_sort_articles("https://techcrunch.com/feed/")


for article in articles:
    if not Posts.objects.filter(pub_date=article['pubDate']).exists():
        url = article['link']
        html = scrape_content(url)
        print("--"*50)
        print(html)
        print('=='*50)
        meta_response = model.generate_content(f'{html} \n {prompt}')
        val = clean(meta_response.text)
        print(val)
        meta_response = eval(val)  # Check that the response
        print("--"*50)
        print(meta_response)
        content = model.generate_content(f"{html} \n Re-write the every paragraph in above html content in engaging way and easy to understand, in atleast 500 words. without title or main heading.")
        p = Posts(post_title=meta_response['title'], post_content=content.text, 
                post_keywords=",".join(meta_response['keywords']), 
                post_meta_tag=",".join(meta_response['meta']),
                pub_date = article['pubDate'],
                author = article['author'],
                # img_src = json.dumps(meta_response['images'])
                img_src = meta_response['images'][0]['src'],
                alt_text = meta_response['images'][0]['alt'],
                
                )
        
        p.save()
        print('-'*10, "DONE", "--"*10)
    else:
        print("--"*12, "Exsists", '***'*12)

print('completed')

# for i in Posts.objects.all():
#     print(i)