from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

BASE_URL = 'https://www.theverge.com/laptop-review'

def get_URL(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    return soup

def crawl_verge(url):
    soup = get_URL(url)
    articles = soup.find_all('div', class_='c-entry-box--compact c-entry-box--compact--featured')
    data = []
    for article in articles:
        d = {'title':'','link':'','image_url':'','description':''}
        try:
            d['title'] = article.h2.string
            d['link'] = article.a['href'] 
            if article.img:
                d['image_url'] = article.find_all('img')[1]['src']
            d['description'] = article.p.string
        except:
            pass
        data.append(d)
    return data

@app.route('/')
def home():
    data = crawl_verge(BASE_URL)
    return render_template('base.html',data = data)

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000, debug=True)
 