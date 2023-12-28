import requests
import sys
from bs4 import BeautifulSoup
import json
import datetime
def getRSSNews(rss_link):
    r = requests.get(rss_link)
    return r.text

def getCompleteArticle(link_to_article_html):
    desc_soup=BeautifulSoup(link_to_article_html,'html.parser')
    if desc_soup.a != None:
        article_link = desc_soup.a.get('href')
        r = requests.get(article_link)
        article_soup = BeautifulSoup(r.text,'html.parser')
        all_script_tags = article_soup.find_all('script')
        for script in all_script_tags:
            if script.text.startswith('{'):
                json_obj = json.loads(script.text)
                if json_obj != None:
                    if "articleBody" in json_obj.keys():
                        return(json_obj["articleBody"])
def get_news_array(rss_text):
    soup = BeautifulSoup(rss_text,'xml')
    all_items = soup.find_all('item')
    news_array = []
    for i in all_items:
        title = i.title.text
        link_to_article_html = i.description.text
        complete_article=getCompleteArticle(link_to_article_html)
        news_dict = {"title":title,
                     "complete_article":complete_article
                    }
        news_array.append(news_dict)
    return news_array
def get_html_text(news_array):
    complete_html_text="<dl>"
    for item in news_array:
       complete_html_text += "<dt><h3>"+item["title"]+"</h3></dt>"
       complete_html_text += "<dd><h5>"+(item["complete_article"] if item["complete_article"] else "Nothing Here")+"</h5></dd>"
    complete_html_text+="</dl>"
    return complete_html_text
rss_link = 'http://timesofindia.indiatimes.com/rssfeeds/-2128936835.cms'
rss_link_hindu = 'https://www.thehindu.com/news/national/?service=rss'
rss_text = getRSSNews(rss_link)
news_array = get_news_array(rss_text)
complete_html_text = get_html_text(news_array)
file_path = "/Users/abhishekdantale/Library/Mobile Documents/com~apple~CloudDocs/News_Article_Daily/"
file=open(file_path + datetime.datetime.now().strftime("%m_%d_%Y_%H_%M_%S") +".html","w",encoding="utf-8")
file.write(complete_html_text)
file.close()
