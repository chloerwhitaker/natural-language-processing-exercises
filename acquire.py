#!/usr/bin/env python
# coding: utf-8

# # Acquire Data through Web Scraping Functions
# 

# ### imports

# In[63]:


import requests
from bs4 import BeautifulSoup
import pandas as pd
from time import strftime


# ### Codeup Blog Scraping Functions

# In[65]:


# https://codeup.com/blog/


# In[74]:


# function to get all links from the main blog page

def get_blog_links():
    
    '''
    This function returns a list of all the urls linked on Codeup's main blog page.
    '''
    
    # imports
    import requests
    from bs4 import BeautifulSoup
    
    response = requests.get("https://codeup.com/blog/", headers={"user-agent": "Codeup DS Hopper"})
    soup = BeautifulSoup(response.text)
    links = [link.attrs["href"] for link in soup.select(".more-link")]
    return links


# In[89]:


# use function to get list of links
# get_blog_links()


# In[76]:


def parse_codeup_blog_article(url):
    
    '''
    This function: 
    takes url of blog post,
    extracts info
    returns the specified info as a dictionary
    '''
    
    # imports
    import requests
    from bs4 import BeautifulSoup
    
    response = requests.get(url, headers={"user-agent": "Codeup DS Hopper"})
    soup = BeautifulSoup(response.text)
    return {
        "title": soup.select_one(".entry-title").text,
        "published": soup.select_one(".published").text,
        "content": soup.select_one(".entry-content").text.strip(),
    }


# In[77]:


url = 'https://codeup.com/dallas-newsletter/codeup-dallas-open-house/'


# In[90]:


#parse_codeup_blog_article(url)


# In[79]:


# return blog article info as a df
def get_blog_articles_info():
    
    '''
    This function: 
    uses get_blog_links to get blog post links from the main Codeup blog page,
    extracts info using parse_codeup_blog_article,
    returns the specified info as a df where each row contains a seperate blog title
    '''
    
    # imports
    import requests
    from bs4 import BeautifulSoup
    
    links = get_blog_links()
    df = pd.DataFrame([parse_codeup_blog_article(link) for link in links])
    return df


# In[91]:


# get_blog_articles_info()


# To save this info so that if the website is updated, it won't change my data during exploration etc:

# In[92]:


# save to json
# today = strftime('%Y-%m-%d')
# get_blog_articles().to_json(f'codeup_blog_{today}.json')


# ### inshorts Scraping Functions

# In[83]:


def parse_news_card(card):
    'Given a news card object, returns a dictionary of the relevant information.'
    card_title = card.select_one('.news-card-title')
    output = {}
    output['title'] = card_title.find('a').text.strip()
    output['published'] = card_title.select_one('.time').attrs['content']
    output['author'] = card_title.select_one('.author').text
    output['content'] = card.select_one('.news-card-content').div.text.strip()
    return output


def parse_inshorts_page(url):
    '''Given a url, returns a dataframe where each row is a news article from the url.
    Infers the category from the last section of the url.'''
    category = url.split('/')[-1]
    response = requests.get(url, headers={'user-agent': 'Codeup DS'})
    soup = BeautifulSoup(response.text)
    cards = soup.select('.news-card')
    df = pd.DataFrame([parse_news_card(card) for card in cards])
    df['category'] = category
    return df

def get_inshorts_articles():
    '''
    Returns a dataframe of news articles from the business, sports, technology, and entertainment sections of
    inshorts.
    '''
    url = 'https://inshorts.com/en/read/{}'
    categories = ['business', 'sports', 'technology', 'entertainment']
    df = pd.concat([parse_inshorts_page(url.format(cat)) for cat in categories])
    df = df.reset_index(drop=True)
    return df


# To save this info so that if the website is updated, it won't change my data during exploration etc:

# In[93]:


# today = strftime('%Y-%m-%d')
# get_inshorts_articles().to_json(f'inshorts-{today}.json')


# In[94]:


# df = pd.read_json('inshorts-2022-02-07.json')


# In[95]:


# df.head()

