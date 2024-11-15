from flask import Flask, render_template, request, redirect, url_for
from transformers import pipeline
import json
import requests

app = Flask(__name__)

# Load the BART summarization model
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

@app.route('/')
def home():
    return render_template('home.html')


def summarize_article(article_text):
    if len(article_text) > 512:  # BART works best with texts shorter than 512 tokens
        article_text = article_text[:512]  # Truncate the text for summarization
    
    summary = summarizer(article_text, max_length=130, min_length=30, do_sample=False)
    return summary[0]['summary_text']

def save_summaries_to_file(summaries, filename='summaries.json'):
    with open(filename, 'w') as f:
        json.dump(summaries, f, indent=4)

def get_news(topic, num_articles=5):
    # Example API call to a news service (replace with actual API)
    api_key = '385b63a94fac4ef480bc3ff9fe850147'  # Replace with your actual API key
    url = f'https://newsapi.org/v2/everything?q={topic}&pageSize={num_articles}&apiKey={api_key}'
    
    response = requests.get(url)
    articles = response.json().get('articles', [])
    
    # Format articles to match the expected structure
    formatted_articles = []
    for article in articles:
        formatted_articles.append({
            'title': article['title'],
            'source': {'name': article['source']['name']},
            'url': article['url'],
            'description': article['description'] or article['content']  # Fallback to content if description is empty
        })
     
    return formatted_articles

@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        topic = request.form.get('topic', 'climate change')  # Get topic from form
        articles = get_news(topic)
        
        summaries = []
        for article in articles:
            summary = summarize_article(article['description'] or '')
            summaries.append({
                'title': article['title'],
                'summary': summary,
                'url' : article['url']
            })
        
        save_summaries_to_file(summaries)
        return render_template('index.html', summaries=summaries, topic=topic)

    return render_template('index.html', summaries=None, topic=None)

if __name__ == '__main__':
    app.run(debug=True)
